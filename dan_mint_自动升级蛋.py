import requests
import json

class RequestProcessor:
    def __init__(self, proxy_file='config/proxy.txt', address_file='config/address.txt'):
        self.url = 'https://bitomokx.irys.xyz/'
        self.first_next_action = '7f266b078f00a6308f787e8747a6d668ac06e38ca2'
        self.repeat_next_action = '7fb85344a1ee49e62581b509d66d4445f1fce2c2c5'
        self.repeat_count = 5
        self.base_headers = {
            'accept': 'text/x-component',
            'accept-language': 'en-GB,en;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'next-router-state-tree': '["",{"children":["__PAGE__":{},"/","refresh"]},null,null,true]',
            'origin': 'https://bitomokx.irys.xyz',
            'priority': 'u=1, i',
            'referer': 'https://bitomokx.irys.xyz/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-deployment-id': 'dpl_8V8sDbT5y75dADDLSweyEdygRdV6'
        }
        self.cookies = {
            '_ga': 'GA1.1.1117769145.1753144161',
            '_ga_N7ZGKKSTW8': 'GS2.1.s1753144160$o1$g1$t1753144244$j60$l0$h0',
            '_ga_B8H17MTRYM': 'GS2.1.s1753226792$o2$g1$t1753226842$j10$l0$h0'
        }
        self.proxies_list = self.read_file_lines(proxy_file)
        self.addresses_list = self.read_file_lines(address_file)
        self.validate_files()

    def read_file_lines(self, file_path):
        """读取文件内容并返回非空行列表"""
        try:
            with open(file_path, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"错误：文件 {file_path} 未找到。")
            return []

    def validate_files(self):
        """验证代理和地址数量是否匹配"""
        if len(self.proxies_list) != len(self.addresses_list):
            print(f"错误：代理数量 ({len(self.proxies_list)}) 与地址数量 ({len(self.addresses_list)}) 不匹配。")
            exit(1)

    def send_request(self, address, proxy, next_action, iteration=None):
        """发送单个POST请求"""
        proxy_dict = {'http': proxy, 'https': proxy}
        headers = self.base_headers.copy()
        headers['next-action'] = next_action
        data = json.dumps([address])
        
        try:
            if iteration:
                print(f"正在处理地址 {address}，使用 next-action {next_action}（第 {iteration}/{self.repeat_count} 次），代理 {proxy}")
            else:
                print(f"正在处理地址 {address}，使用 next-action {next_action}，代理 {proxy}")
            response = requests.post(self.url, headers=headers, cookies=self.cookies, data=data, proxies=proxy_dict, timeout=10)
            if iteration:
                print(f"地址 {address}（next-action: {next_action}，第 {iteration} 次）的响应：状态码 {response.status_code} - {response.text}")
            else:
                print(f"地址 {address}（next-action: {next_action}）的响应：状态码 {response.status_code} - {response.text}")
        except requests.RequestException as e:
            if iteration:
                print(f"处理地址 {address}，next-action {next_action}（第 {iteration} 次），代理 {proxy} 时出错：{e}")
            else:
                print(f"处理地址 {address}，next-action {next_action}，代理 {proxy} 时出错：{e}")
            return False
        return True

    def process_requests(self):
        """处理所有地址的请求"""
        for address, proxy in zip(self.addresses_list, self.proxies_list):
            # 第一次请求
            success = self.send_request(address, proxy, self.first_next_action)
            if not success:
                continue  # 如果第一次请求失败，跳到下一个地址

            # 重复5次请求
            for i in range(self.repeat_count):
                self.send_request(address, proxy, self.repeat_next_action, iteration=i+1)

if __name__ == "__main__":
    processor = RequestProcessor()
    processor.process_requests()
