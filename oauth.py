"""生成 Instagram OAuth 授權 URL"""
import urllib.parse

APP_ID = "1218345513805288"
REDIRECT_URI = "https://developers.facebook.com/tools/explorer/"
SCOPES = "instagram_basic,instagram_content_publish,pages_read_engagement"

print("=" * 50)
print("Instagram OAuth 授權流程")
print("=" * 50)

# 生成授權 URL
auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={APP_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope={urllib.parse.quote(SCOPES)}&response_type=code"

print(f"\n請訪問以下 URL 並授權：\n")
print(auth_url)
print(f"\n{'=' * 50}")
print("授權完成後，你會被重定向到：")
print(f"{REDIRECT_URI}?code=XXXXX")
print("\n把 URL 列給我，我幫你換 token")
