import sys
import requests
from base64 import b64encode
from nacl import encoding, public
import json

repo_name = sys.argv[1]
public_key = sys.argv[2]
public_key_id = sys.argv[3]
secret_name = sys.argv[4]
secret_value = sys.argv[5]
github_token = sys.argv[6]

def encrypt(public_key: str, secret_value: str) -> str:
  """Encrypt a Unicode string using the public key."""
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")


encrypted_secret = encrypt(public_key, secret_value)


print('Setting secret {secret_name} for repository {repo}'.format(secret_name=secret_name, repo=repo_name))

put_url = 'https://api.github.com/repos/{repo_name}/actions/secrets/{secret_name}'.format(repo_name=repo_name, secret_name=secret_name)
headers = {'Accept': 'application/vnd.github+json', 'Authorization': 'Bearer {token}'.format(token=github_token)}
data = json.dumps({"encrypted_value": encrypted_secret, "key_id": public_key_id })

res = requests.put(put_url, data, headers=headers)

print('Status Code: {status_code}'.format(status_code=res.status_code))

print(res.content)

if not res.ok:
  raise Exception('Exception creating repo secret')
