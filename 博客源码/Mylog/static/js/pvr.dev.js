/*
Author: WangShihan
Email: 3443327820@qq.com
Date: 2022-10-14
Description: record
*/

function genUID(length) {
  var result = '';
  var characters = '0123456789';
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

function getSessionInfoByName(name) {
  let value = sessionStorage.getItem(name);
  if (value === null || value == '') {
    value = genUID(12);
    sessionStorage.setItem(name, value);
  }
  return value;
}

function generateIOI() {
  const now = new Date();
  let uid = getLocalInfoByName('uid');

  if (!uid) {
    uid = genUID(12);
    setLocalInfo('uid', uid, 60 * 60 * 24 * 365);
  }

  let ioi = {
    uid: getLocalInfoByName('uid'),
    sid: getSessionInfoByName('sid'),
    vid: getSessionInfoByName('vid'),
    sw: window.screen.width,
    tz: now.getTimezoneOffset(),
    ts: now.getTime(),
    st: 0,
    url: window.location.href,
    tt: document.title,
    lang: navigator.userLanguage || navigator.language,
    ref: document.referrer,
  };

  return ioi;
}

function setLocalInfo(key, value, age) {
  if (navigator.cookieEnabled) {
    document.cookie = `${key}=${value};max-age=${age};path=/;`;
  } else {
    localStorage.setItem(key, value);
  }
}

function getLocalInfoByName(name) {
  if (navigator.cookieEnabled) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].split('=');
      if (cookie[0].trim() === name) {
        return cookie[1];
      }
    }
  } else {
    return localStorage.getItem(name);
  }
}

function request(payload) {
  fetch('/mylog/ppv/collect', {
    method: 'POST',
    keepalive: true,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
    .then(res => {
      if (!res.ok) {
        throw new Error('request error');
      } else {
        return res.json();
      }
    })
    .then(res => {})
    .catch(err => {
      console.warn(err);
    });
}

function detectDeviceIsPC() {
  // 使用正则表达式匹配常见的移动设备关键词
  const mobileKeywords = [
    'Android',
    'webOS',
    'iPhone',
    'iPad',
    'iPod',
    'BlackBerry',
    'Windows Phone',
  ];
  return !mobileKeywords.some(keyword => navigator.userAgent.match(new RegExp(keyword, 'i')));
}

function enter() {
  const ioi = generateIOI();
  request(ioi);
}

function leave() {
  const ioi = generateIOI();
  sessionStorage.setItem('vid', '');
  ioi.st = 1;
  request(ioi);
}

// 绑定事件
(function () {
  if (detectDeviceIsPC()) {
    document.addEventListener('DOMContentLoaded', () => {
      enter();
    });
    window.addEventListener('beforeunload', () => {
      leave();
    });
  } else {
    window.addEventListener('pageshow', () => {
      enter();
    });
    window.addEventListener('pagehide', () => {
      leave();
    });
  }
})();


