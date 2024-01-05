from pathlib import Path



# # p = Path('api_yambd/static/data/category.csv')
# p = Path()

# p.resolve

# print(p)

BASE_DIR = Path.cwd() / 'api_yamdb' / 'static' / 'data'
print(BASE_DIR)
TEMPLATE_DIR = BASE_DIR / 'category.csv'
print(TEMPLATE_DIR)

with TEMPLATE_DIR.open('r') as f:
    content = f.read()

print(content)