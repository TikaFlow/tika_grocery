// ==UserScript==
// @name         追剧防猝死
// @namespace    https://blog.tika-flow.com/
// @version      1.0
// @description  在视频右上角显示系统时间，以免废寝忘食
// @author       Tika Flow
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 检测 video 标签
    var video = document.querySelector('video');
    if (!video) return;

    // 创建 div 对象
    var timeDiv = document.createElement('div');
    timeDiv.setAttribute('style', 'position:absolute; top:0; right:0; padding:4px; font-size:24px; color:#fff; background-color:rgba(0, 0, 0, 0.2); border-radius:5px');
    video.parentElement.appendChild(timeDiv);

    // 生成时间
    function updateTime() {
        // 获得时间
        var now = new Date();

        // 设置时间
        /*
        var hours = now.getHours().toString().padStart(2, '0');
        if(hours <= 6){
            timeDiv.style.fontSize = '360px';
            timeDiv.style.color = 'red';
        }
        */
        // var minutes = now.getMinutes().toString().padStart(2, '0');
        // var seconds = now.getSeconds().toString().padStart(2, '0');
        // timeDiv.textContent = hours + ':' + minutes + ':' + seconds;
        timeDiv.innerHTML = now.toLocaleTimeString();
    }

    updateTime();
    setInterval(updateTime, 1000);
})();
