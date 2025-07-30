from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """PWA用のアイコンを生成"""
    # 新しい画像を作成
    img = Image.new('RGBA', (size, size), (108, 92, 231, 255))
    draw = ImageDraw.Draw(img)
    
    # グラデーション効果
    for y in range(size):
        alpha = int(255 * (1 - y / size))
        color = (108, 92, 231, alpha)
        draw.line([(0, y), (size, y)], fill=color)
    
    # 中央にアイコンを描画
    icon_size = max(size // 4, 8)  # 最小サイズを確保
    x = (size - icon_size) // 2
    y = (size - icon_size) // 2
    
    # シンプルなアイコン（栄養を表す葉っぱ）
    draw.ellipse([x, y, x + icon_size, y + icon_size], fill=(255, 255, 255, 200))
    
    # 内側の円（より小さく）
    inner_size = max(icon_size - 4, 4)
    inner_x = (size - inner_size) // 2
    inner_y = (size - inner_size) // 2
    draw.ellipse([inner_x, inner_y, inner_x + inner_size, inner_y + inner_size], fill=(0, 255, 0, 255))
    
    # 保存
    img.save(f'static/icons/{filename}')
    print(f'アイコン生成: {filename}')

def main():
    """メイン関数"""
    # 必要なサイズのアイコンを生成
    icons = [
        (16, 'icon-16x16.png'),
        (32, 'icon-32x32.png'),
        (72, 'icon-72x72.png'),
        (96, 'icon-96x96.png'),
        (128, 'icon-128x128.png'),
        (144, 'icon-144x144.png'),
        (152, 'icon-152x152.png'),
        (192, 'icon-192x192.png'),
        (384, 'icon-384x384.png'),
        (512, 'icon-512x512.png')
    ]
    
    for size, filename in icons:
        create_icon(size, filename)
    
    print('すべてのアイコンが生成されました！')

if __name__ == '__main__':
    main() 