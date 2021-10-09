import json, os, time
from solana.rpc.api import Client
from solana.rpc.types import MemcmpOpts
import pandas as pd

def connect_to_rpc(solana_RPC):
    try:
        solana_client = Client(solana_RPC)
        connection_state = solana_client.is_connected()
    except:
        print(f'Connection refused to RPC {solana_RPC}')
        return None

    if connection_state is False or connection_state is None:
        print(f'Connection \033[1;31;40m refused \033[0;37;40m to RPC: {solana_RPC}')
        return None
    else:
        print(f'Connection \033[1;32;40m succeeded \033[0;37;40m to RPC: {solana_RPC}')
        return solana_client

## Get accounts that once held the token_id
def get_token_account_info(token_id):
    memcmp_opts = [
        MemcmpOpts(offset=0, bytes=token_id),
    ]
    program_account_json = solana_client.get_program_accounts("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", data_size=165, encoding="jsonParsed", memcmp_opts=memcmp_opts)
    print(f"\nresponse is: {json.dumps(program_account_json, indent=4)}")
    return program_account_json

if __name__ == '__main__':

    #solana_RPC = "https://api.devnet.solana.com"
    solana_RPC = "https://api.mainnet-beta.solana.com"
    solana_client = connect_to_rpc(solana_RPC)

    token_ids = open('full.txt', 'r').read().replace('[','').replace(']','').replace('"','').strip().split(',')
    
    account_list = []
    for token_id in token_ids:
        token_id = token_id.replace('\n', '').strip()
        program_account_info = get_token_account_info(token_id)

        ## Loop through all account that once possessed the current token
        ## To find the one that hold it at the moment
        print("\n\nRetrieving tokens informations...")
        
        for account in program_account_info['result']:
            if int(account['account']['data']['parsed']['info']['tokenAmount']['amount']) > 0:
                owner = account['account']['data']['parsed']['info']['owner']
                print(f"\n{owner} own currently the token {token_id}")
                account_list.append(owner)
                break
        time.sleep(1)
           
    
    print(len(token_ids))
    print(len(account_list))
    final_data = []
    for (token, holder) in zip(token_ids, account_list):
        final_data.append({token:holder})
    print(final_data)
    f = open('final.json', 'w')
    f.write(str(final_data))
    f.close()