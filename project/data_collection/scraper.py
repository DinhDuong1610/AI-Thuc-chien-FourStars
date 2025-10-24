import requests
from bs4 import BeautifulSoup

def fetch_article_text(url):
    """
    Lấy toàn bộ nội dung văn bản từ một URL bài báo.
    LƯU Ý: Cấu trúc mỗi trang web là khác nhau, bạn có thể cần phải
    thay đổi thẻ và class để lấy đúng nội dung.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Ví dụ cho trang vtv.vn (cần kiểm tra lại class thực tế)
        # Bấm F12 trên trình duyệt để xem cấu trúc HTML của trang
        title = soup.find('h1', class_='title-detail')
        content_div = soup.find('div', class_='content-detail')
        
        if not title or not content_div:
            print(f"Không tìm thấy tiêu đề hoặc nội dung cho URL: {url}")
            return None
            
        # Lấy tất cả các đoạn văn bản và nối chúng lại
        paragraphs = content_div.find_all('p')
        full_text = title.get_text(strip=True) + "\n\n"
        full_text += "\n".join([p.get_text(strip=True) for p in paragraphs])
        
        return full_text
        
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tải URL {url}: {e}")
        return None

if __name__ == "__main__":
    # Danh sách các URL được phép
    # VTV_URL = "https://vtv.vn/chinh-tri/bai-viet-mau.htm" # Thay bằng URL thật
    # DANGCONGSAN_URL = "https://dangcongsan.vn/bai-viet-mau.htm" # Thay bằng URL thật
    URL = "https://nda.org.vn"
    
    print(f"Đang crawl dữ liệu từ {URL}...")
    article_content = fetch_article_text(URL)
    
    if article_content:
        # Lưu vào file để sử dụng làm ngữ cảnh cho AI
        output_path = "collected_data/article.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(article_content)
        print(f"Đã lưu nội dung vào {output_path}")