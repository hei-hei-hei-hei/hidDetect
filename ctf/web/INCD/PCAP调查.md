# PCAP调查
调查 PCAP 文件以查找标志。

旗帜由两部分组成
旗帜结构 - XXXX_XX_XXX
根据协议细分，附加的 PCAP 中没有太多内容：

┌──(user@kali)-[/media/sf_CTFs/INCD/pcap_investigation]
└─$ tshark -qz io,phs -r pcap_challenge.pcap

===================================================================
Protocol Hierarchy Statistics
Filter:

null                                     frames:1563 bytes:346009
  ip                                     frames:1563 bytes:346009
    udp                                  frames:20 bytes:3764
      ssdp                               frames:20 bytes:3764
    icmp                                 frames:6 bytes:768
      nbns                               frames:6 bytes:768
    tcp                                  frames:1537 bytes:341477
      tls                                frames:714 bytes:299988
      http                               frames:6 bytes:5011
        data-text-lines                  frames:2 bytes:1290
        json                             frames:1 bytes:1005
      data                               frames:1 bytes:45
===================================================================
查看 TCP 流 14 中的消息：

┌──(user@kali)-[/media/sf_CTFs/INCD/pcap_investigation]
└─$ tshark -r pcap_challenge.pcap -qz follow,tcp,ascii,14

===================================================================
Follow: tcp,ascii
Filter: tcp.stream eq 14
Node 0: 127.0.0.1:55776
Node 1: 127.0.0.1:8000
787
GET / HTTP/1.1
Host: 127.0.0.1
sec-ch-ua: "Chromium";v="111", "Not(A:Brand";v="8"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.65 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Date:MNDU42DDIY4XIWSWHA4GI3KWPFSVGQTOMIZDS22MINBDKYRTKVTWE3KWNRNEGQRQMJ4UE3LBK42WWSKHIVTWE3SWORMW2VTZJFEFE5SJI5HHMYSYIJZVUWCSNRE
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
info: 00110000 00110000 00110111
Connection: close


        601
HTTP/1.1 303 See Other
Date: Sun, 12 Mar 2023 16:45:16 GMT
Content-Type: text/html; charset=UTF-8
X-Content-Type-Options: nosniff
Content-Length: 321
Location: http://127.0.0.1/en-US/
Vary: Accept-Language
Connection: Close
X-Frame-Options: SAMEORIGIN
Server: Splunkd

<!doctype html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><meta http-equiv="refresh" content="1;url=http://127.0.0.1/en-US/"><title>303 See Other</title></head><body><h1>See Other</h1><p>The resource has moved temporarily <a href="http://127.0.0.1/en-US/">here</a>.</p></body></html>

===================================================================
“Date”标头的值似乎很奇怪。解码为 Base32 到 ，然后解码为 base64 到 。要完成该标志，请将“info”标头解码为二进制：。标志是 .cGNhcF9tZV88dmVyeSBnb29kLCB5b3UgbmVlZCB0byBmaW5kIGEgbnVtYmVyIHRvIGNvbXBsZXRlJpcap_me_<very good, you need to find a number to complete007pcap_me_007