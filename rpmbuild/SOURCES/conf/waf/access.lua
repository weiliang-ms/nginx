reques_method = ngx.var.request_method
reques_uri = ngx.var.request_uri
host=ngx.var.http_host
referer=ngx.var.http_referer
user_agent=ngx.var.http_user_agent

-- 判断是否开启waf
if(open_waf == true)
then
    -- host合法性检测
    if(open_check_host == true)then
        host_check(host)
    end

    -- method合法性检测
    if(open_check_method == true)then
        method_check(reques_method)
    end

    -- url合法性检测
    if(open_check_url == true)then
        url_check()
    end

    -- referer合法性检测
    if(open_check_referer == true)then
        referer_check(referer,host)
    end

    -- agent合法性检测
    if(open_check_agent == true)then
        agent_check(user_agent)
    end

    if(open_check_agrs == true)then
        args_check()
    end

    if(open_check_body == true)then
        body_check()
        analysis_body()
    end
end
