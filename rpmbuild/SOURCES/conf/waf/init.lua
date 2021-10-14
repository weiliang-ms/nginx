require 'config'

local ngx_match=ngx.re.match
local unescape=ngx.unescape_uri
open_url_filter=true
open_logging=true

-- 记录debug日志
function record_debug_log(msg)
    if open_logging then
        local logfile = log_path..'/'.."debug.log"
        write(logfile,msg)
    end
end

-- 判断table内是否含有元素
function tableFind(value, tbl)
  for k,v in ipairs(tbl) do
    -- 防止出现空格
    re = string.find(v, value, nil)
    if re ~= nil then
      return true;
    end
  end
    return false;
end

-- 读取规则
function read_rule(path,var)
    local file = assert(io.open(path..var,'r'))
    local result = {};
    for line in file:lines() do
       result[#result+1] = line;
    end
    file:close()
    return(result)
end
-- 读取url拦截规则
local urlrules=read_rule(black_rule_path,'url')
-- 读取agetn拦截规则
local bad_agents=read_rule(black_rule_path,'user-agent')
-- 读取args拦截规则
local bad_args=read_rule(black_rule_path,'args')
-- 读取post body拦截规则
local postrules=read_rule(black_rule_path,'post')
-- 读取http method白名单
local valid_methods=read_rule(white_rule_path,'method')
-- 读取http Host白名单
local valid_hosts=read_rule(white_rule_path,'host')
-- 读取 referer 白名单
local valid_referers=read_rule(white_rule_path,'referer')

-- 获取客户端IP
function get_client_ip()
    local headers=ngx.req.get_headers()
    local ip=headers["X-REAL-IP"] or headers["X_FORWARDED_FOR"] or ngx.var.remote_addr or "0.0.0.0"
    return ip
end

-- 写入文件
function write(file,msg)
    local fd = io.open(file,"ab")
    if fd == nil then return end
    fd:write(msg)
    fd:flush()
    fd:close()
end

-- 记录waf日志
function record_attack_log(identifier)
    if open_logging then
        local realIP = get_client_ip()
        local agent = ngx.var.http_user_agent
        local time=ngx.localtime()
        logformat = "-----".."\n".."ClientIP: "..realIP.."\n".."Host: "..ngx.var.http_host.."\n".."time: "..time.."\n".."uri: "..ngx.var.request_uri.."\n".."User-Agent: "..agent.."\n".."deny_rule: "..identifier.."\n".."-----".."\n"
        local logfile = log_path..'/'.."waf.log"
        write(logfile,logformat)
    end
end

-- 检测方法合法性
function method_check(method)
   record_debug_log(method)
   if tableFind(method,valid_methods) == false
      then
        record_attack_log("BadHttpMethod")
        ngx.exit(405)
   end
end

function fileExtCheck(ext)
    local items = Set(black_fileExt)
    ext=string.lower(ext)
    if ext then
        for rule in pairs(items) do
            if ngx.re.match(ext,rule,"isjo") then
                record_attack_log("file attack with ext "..ext)
            end
        end
    end
    return false
end

function get_boundary()
    
    local header = ngx.req.get_headers()["content-type"]
    if not header then
        return nil
    end

    if type(header) == "table" then
        header = header[1]
    end

    local m = string.match(header, ";%s*boundary=\"([^\"]+)\"")
    if m then
        return m
    end

    return string.match(header, ";%s*boundary=([^\",;]+)")
end

-- 校验url
function url_check()
    if open_url_filter then
        for _,rule in pairs(urlrules) do
            if rule ~="" and ngx_match(ngx.var.request_uri,rule,"isjo") then
                record_attack_log("BadUrl")
                -- ngx.redirect("/deny")
                ngx.exit(402)
                return true
            end
        end
    end
    return false
end

-- 校验Host合法性
function host_check(host)
    if tableFind(host,valid_hosts) == false
      then
	record_attack_log("BadHost")
	ngx.exit(444)
    end
end

-- 校验Referer合法性
function referer_check(refer,host)
    if refer ~= nil and string.find(refer,host) == nil 
      then 
        if tableFind(refer,valid_referers) == false
          then
	    record_attack_log("BadRefer")
            ngx.exit(444)
        end
    end
end

-- 校验Agent合法性
function agent_check(user_agent)
    if user_agent ~= nil then
        for _,rule in pairs(bad_agents) do
	    if rule ~="" and ngx_match(user_agent,rule,"isjo") then
                record_attack_log("BadAgent")
		ngx.exit(402)
	    end
        end
    end
end

function args_check()
    for _,rule in pairs(bad_args) do
        local args = ngx.req.get_uri_args()
        for key, val in pairs(args) do
            if type(val)=='table' then
                 local t={}
                 for k,v in pairs(val) do
                    if v == true then
                        v=""
                    end
                    table.insert(t,v)
                end
                data=table.concat(t, " ")
            else
                data=val
            end
            if data and type(data) ~= "boolean" and rule ~="" and ngx_match(unescape(data),rule,"isjo") then
		record_attack_log("BadArgs")
		ngx.exit(402)
            end
        end
    end
end

function analysis_body()
    if ngx.var.request_method =="POST" then
	-- 获取body大小,为空视为攻击
        local content_length=tonumber(ngx.req.get_headers()['content-length'])
	if content_length == 0 then
	    record_attack_log("空body")
            ngx.exit(402)
	end
    end
end

function body_check(data)
    for _,rule in pairs(postrules) do
        if rule ~="" and data~="" and ngx_match(unescape(data),rule,"isjo") then
	    record_attack_log("BadBody")
            return true
        end
    end
    return false
end
