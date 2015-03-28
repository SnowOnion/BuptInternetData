/**
 * 这是从登录后的 10.3.8.211 页面中找出的流量计算部分，非常炸裂。我们的工具没有管它是怎么算的。
 * 
 */
time = '7161      ';
flow = '4444413   ';
fee = '424200    ';

flow0 = flow % 1024;
flow1 = flow - flow0; // flow1/1024 是整的MB数
flow0 = flow0 * 1000;
flow0 = flow0 - flow0 % 1024;
fee1 = fee - fee % 100;
flow3 = '.';
if (flow0 / 1024 < 10)
    flow3 = '.00';
else {
    if (flow0 / 1024 < 100)
        flow3 = '.0';
}

console.log('flow0', flow0, 'flow1', flow1, 'flow3', flow3);

document.write("已使用时间 Used time : " + time + " Min");
document.write("已使用校外流量 Used internet traffic : " + flow1 / 1024 + flow3 + flow0 / 1024 + " MByte");
document.write("余额 Balance : " + "RMB" + fee1 / 10000); // 二进制和十进制夹杂 感觉哪里不对

// 操 我管他怎么朋克干嘛 我会算不就行了