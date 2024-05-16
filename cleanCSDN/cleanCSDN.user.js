// ==UserScript==
// @name         CSDN免登陆免关注无复制限制
// @namespace    https://blog.tika-flow.com/
// @version      1.0
// @description  CSDN解除复制限制，去掉登陆提示，解除关注才能查看全文的限制，删除一些广告
// @author       Tika Flow
// @match       *://*.blog.csdn.net/*
// @match       *://*.zhihu.com/*
// @require      https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js
// @icon         https://wba.tika-flow.com/ref/img/avatar.png
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    $(document).ready(function() {
        function init(){
            // 免关注
            $('#article_content')?.removeAttr("style");
            $('.hide-article-box')?.remove();
            // 免登录
            $('.passport-login-container')?.remove();
            $('.Modal-closeButton')[0]?.click(); // 知乎
            // 可复制
            $('code')?.css("userSelect", "text");
            $(document).off('copy');
            $('div#content_views')?.off('copy');
            $('div.blog-content-box')?.off('copy');
            $('.hljs-button')?.remove();

            // 左广告
            $('.box-shadow')?.remove(); // 广告
            $('#footerRightAds')?.remove(); // 广告
            $('#asideWriteGuide')?.remove(); // 推广
            $('#asideNewComments')?.remove(); // 评论
            $('#asideNewNps')?.remove(); // 打分

            // 上广告
            $('.toolbar-advert')?.remove();

            // 右侧
            $('.sidetool-writeguide-box')?.remove(); // 小猴子
            $('.csdn-side-toolbar ')?.remove(); // 侧边栏
            $('.programmer1Box')?.remove(); // 广告
            $('#recommendAdBox')?.remove(); // 广告

            // 底部
            $('.recommend-box')?.remove(); // 推荐
            $('#pcCommentBox')?.remove(); // 评论
            $('#recommendNps')?.remove(); // 打分
        }
        init();

        // 防反弹
        $(document).on('DOMNodeInserted', function() {
            init();
        });
    });
})();