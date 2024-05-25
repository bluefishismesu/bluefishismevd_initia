🚀 Excited to announce our POS Validator bluefishismevd on the Inita blockchain is now live! 🔐

Ensure the security and reliability of transactions with our Validator. 

Join us and become part of the Inita blockchain network to enjoy the benefits!

Learn more: [https://github.com/bluefishismesu/bluefishismevd_initia]

#Blockchain #POS #Validator #Inita


# Good PEERS
## It has shown improvement for me.
TOP 30 BLOCK HEIGHT 336635 - 328670
```bash
PEERS="9187df134f7c52a60fe9e320d5cb1182d75e549a@51.222.10.137:53456,09906124eae99c3fc9a1371b27aa41568a7574cf@65.108.128.89:26656,b5d5108a5b11b55fa7725569517a2d19ff6ed096@135.181.213.169:26656,3194727c8195c5819093b677a982be0d512fa033@89.187.191.103:26656,bbed6acb41d66403e27294471f742d56b7929740@84.32.186.161:26656,0763b4a372cc0c2c50ceeca3205fa47a770ba489@37.27.118.144:27656,78cd568357be4e89a25cbb91dadd69153d27319f@37.27.100.124:27656,bdda79344c3d0a1399fc1df5afa3b3eeed42b030@37.27.100.171:27656,d0e59cf5607ed3241e193995f344c80c536a3b9f@37.27.119.209:27656,2e120200e1ce0e5db42f8de0664304bc6e780c3b@85.190.240.122:25756,20bc0588df61ad3027919035ba2a4403f3e58d1c@65.108.129.151:26656,5f8b1929e71923d3466eee1178922eb15cec5210@93.189.29.18:26656,b54d4bdf047f0c60a965b1f9b03bdcf58c79e7a3@158.220.113.67:26656,42ef41a1c59ca4078123e2a204d63ddcec58a3a2@149.56.107.219:53456,01b9a8ca119b272c9c903b4dcaabd9a9ed3882f9@86.57.164.166:26656,19d1b74e90dac092160b423adb07b7e292bb6056@148.113.6.161:26656,1d7009d9a98534134d1f11e37ac3117a2ffa5664@95.31.9.170:26656,88fc1ceb74ae35907b96fde508fb00ed16dc7fb9@95.216.23.165:26656,9bd20099d508f40d5b0f803e36613fb4d2b5cd82@147.45.197.205:26656,01c5d72c07aa846283494d9fe023c829c84bfdcc@65.109.126.231:25756,a8820aa280a4aeceae186651b824fc6db973747f@148.113.9.177:26656,7f45e6641b481e7b6bd4c19a1cb603d84d7b1765@51.195.60.216:26656,7c1176aec5e64985f1d979eff8a0130b20620a40@135.125.189.52:26656,d9ddaebdb1ac17d0b13d5b56a417585274e9b740@195.179.231.90:25756,0bb11eaf1867a11c2fbbbe250c4d33850329a2df@109.205.181.106:26656,39fdd2b916bd54b36d4cf0bf491014f1d20b12d7@51.178.79.51:26656,b858c16307a9730007d67918272b4b81bfdccee9@136.243.75.46:51656,ab137f5c7eed1bb5172bd7cbe642ec17180ec397@193.34.213.155:33756,54e3a3fd945e1769806a3c38fa6c708ee3e6dc15@194.60.87.37:27656,911e6dc9b21cc37bf6c0b09e86a426304a927cfa@51.91.31.25:26656"
sed -i 's|^persistent_peers *=.*|persistent_peers = "'$PEERS'"|' $HOME/.initia/config/config.toml
```


# Tools
## peerscheck_with_height.py
PEERS with Good Height Generate

## peerscheck.py

This Python tool is designed to check the connectivity and response times of a list of IP addresses and ports provided in a text file. It will then keep the top 40 connections with the lowest response times and save them to a new file.


# Commands
##Restart the node
```bash
sudo systemctl restart initiad
```

##Log the node
```bash
sudo journalctl -u initiad -f -o cat
```

##Check the synchronization status
```bash
initiad status | jq -r .sync_info
```

##Check the BLOCK HEIGHT
```bash
local_height=$(initiad status | jq -r .sync_info.latest_block_height); network_height=$(curl -s https://rpc-initia-testnet.trusted-point.com/status | jq -r .result.sync_info.latest_block_height); blocks_left=$((network_height - local_height)); echo "Your node height: $local_height"; echo "Network height: $network_height"; echo "Blocks left: $blocks_left"
```

##Check peers connected to your node
```bash
curl -Ss localhost:$RPC_PORT/net_info  | jq .result.n_peers
```

