import os
from api_client import (
    generate_text, generate_image, generate_speech, generate_video_workflow,
    save_text, save_image, save_audio, save_video, check_api_spend
)

# --- CẤU HÌNH ĐƯỜNG DẪN THƯ MỤC LƯU SẢN PHẨM ---
# Đảm bảo các thư mục này đã được tạo trong final_product/
OUTPUT_DIR = "../final_product"
D1_VIDEO_DIR = os.path.join(OUTPUT_DIR, "D1_Video_Ban_Tin")
D2_COMIC_DIR = os.path.join(OUTPUT_DIR, "D2_Truyen_Tranh")
D3_INFOGRAPHIC_DIR = os.path.join(OUTPUT_DIR, "D3_Infographic")
D4_WEBSITE_DIR = os.path.join(OUTPUT_DIR, "D4_Website")
D5_LYRIC_VIDEO_DIR = os.path.join(OUTPUT_DIR, "D5_Lyric_Video")
D6_EVENT_PLAN_DIR = os.path.join(OUTPUT_DIR, "D6_Ke_Hoach_Event")
D7_REPORT_DIR = os.path.join(OUTPUT_DIR, "D7_Bao_cao")
D8_GAME_DIR = os.path.join(OUTPUT_DIR, "D8_Game")
D9_FLYER_DIR = os.path.join(OUTPUT_DIR, "D9_To_Gap")


# ==============================================================================
# ==                       WORKFLOW CHO CÁC DẠNG ĐỀ                           ==
# ==============================================================================

def workflow_de_1_video_ban_tin():
    """
    Kịch bản mẫu cho Dạng đề 1: Tạo video bản tin truyền hình.
    """
    print("\n--- BẮT ĐẦU WORKFLOW DẠNG ĐỀ 1: VIDEO BẢN TIN ---")
    
    # 1. Sinh kịch bản lời dẫn cho MC
    prompt_kich_ban = """
    Viết một kịch bản lời dẫn cho một MC truyền hình (nữ, giọng miền Bắc) để tổng kết các hoạt động chào mừng 80 năm Quốc khánh 2/9/2025 trên cả nước. 
    Lời dẫn cần trang trọng, hào hùng, súc tích và có chứa câu chính xác: 'Các hoạt động chính kỷ niệm 80 năm Quốc khánh 2/9 vào ngày 2 tháng 9 năm 2025'.
    Độ dài khoảng 150-200 từ để phù hợp với video 80 giây.
    """
    mc_script = generate_text(prompt_kich_ban)
    if mc_script:
        save_text(mc_script, os.path.join(D1_VIDEO_DIR, "kich_ban_mc.txt"))

        # 2. Chuyển kịch bản thành giọng nói (audio)
        mc_audio = generate_speech(mc_script, voice="female_north", speed=1.0)
        if mc_audio:
            save_audio(mc_audio, os.path.join(D1_VIDEO_DIR, "thuyet_minh_mc.mp3"))

    # 3. Tạo hình ảnh nhân vật MC ảo
    prompt_mc_image = "Một nữ MC truyền hình người Việt Nam, khoảng 30 tuổi, mặc áo dài đỏ, đang đứng trong một studio tin tức hiện đại có logo VTV và nền màu xanh dương. Ảnh chân dung, biểu cảm chuyên nghiệp."
    mc_image = generate_image(prompt_mc_image, size="1920x1080", model="dall-e-3") # Kích thước cho video HD
    if mc_image:
        save_image(mc_image, os.path.join(D1_VIDEO_DIR, "hinh_anh_mc.png"))

    # 4. Tạo các cảnh video minh họa
    prompt_video_canh1 = "Một cảnh quay flycam tuyệt đẹp trên không tại quảng trường Ba Đình, Hà Nội vào ngày 2/9/2025. Hàng ngàn người dân vẫy cờ đỏ sao vàng. Không khí trang nghiêm và lễ hội. Chất lượng 4K, điện ảnh."
    video_clip_1 = generate_video_workflow(prompt_video_canh1)
    if video_clip_1:
        save_video(video_clip_1, os.path.join(D1_VIDEO_DIR, "canh_quang_truong_ba_dinh.mp4"))
        
    print("--- HOÀN THÀNH WORKFLOW DẠNG ĐỀ 1 ---")
    print(">>> Nhiệm vụ tiếp theo: Dùng Adobe Premiere để ghép audio, hình ảnh MC và các video clip lại thành một bản tin hoàn chỉnh 80 giây.")


def workflow_de_2_truyen_tranh():
    """
    Kịch bản mẫu cho Dạng đề 2: Sáng tạo truyện tranh (comic).
    """
    print("\n--- BẮT ĐẦU WORKFLOW DẠNG ĐỀ 2: TRUYỆN TRANH ---")
    
    # 1. Sinh ý tưởng kịch bản truyện tranh
    prompt_story = """
    Sáng tạo một kịch bản truyện tranh ngắn (khoảng 5 trang) về chủ đề Quốc Khánh 2/9. 
    Nhân vật chính là một bạn nhỏ tên An và ông nội (một cựu chiến binh). 
    Câu chuyện kể về việc ông giải thích cho An về ý nghĩa của ngày lễ này qua những kỷ vật xưa.
    Kịch bản cần chia rõ từng trang, mỗi trang có mô tả các khung hình (panel) và lời thoại.
    """
    story_script = generate_text(prompt_story)
    if not story_script: return
    save_text(story_script, os.path.join(D2_COMIC_DIR, "kich_ban_truyen.txt"))
    
    # 2. Sinh hình ảnh cho từng trang/khung hình
    character_description = "An là một bé gái 8 tuổi, tóc đen buộc hai bên, mắt to tròn, mặc váy màu vàng. Ông nội khoảng 70 tuổi, tóc bạc, đeo kính, mặc áo sơ mi bộ đội cũ."
    
    prompt_cover = f"Trang bìa truyện tranh. {character_description}. An và ông nội đang đứng ở ban công nhìn ra đường phố cờ hoa ngày 2/9. Tiêu đề: 'Ngày Độc Lập'. Phong cách Ghibli, màu sắc tươi sáng."
    cover_image = generate_image(prompt_cover, size="1024x1792") # Tỷ lệ A4
    if cover_image:
        save_image(cover_image, os.path.join(D2_COMIC_DIR, "trang_01_bia.png"))

    prompt_p2_f1 = f"Khung truyện tranh. {character_description}. Cảnh trong nhà, An tò mò hỏi ông về tấm huân chương cũ. Phong cách Ghibli."
    p2_f1_image = generate_image(prompt_p2_f1, size="1024x1024")
    if p2_f1_image:
        save_image(p2_f1_image, os.path.join(D2_COMIC_DIR, "trang_02_khung_1.png"))
        
    print("--- HOÀN THÀNH WORKFLOW DẠNG ĐỀ 2 ---")
    print(">>> Nhiệm vụ tiếp theo: Dùng Photoshop/Canva để dàn trang, thêm lời thoại vào các khung hình đã tạo.")

def workflow_de_3_infographic():
    """
    Kịch bản mẫu cho Dạng đề 3: Tạo infographic.
    """
    print("\n--- BẮT ĐẦU WORKFLOW DẠNG ĐỀ 3: INFOGRAPHIC ---")

    # 1. Sinh nội dung text cho Infographic
    prompt_content = """
    Tóm tắt các hoạt động chính và ý nghĩa của lễ kỷ niệm 80 năm Quốc khánh 2/9/2025 dưới dạng các gạch đầu dòng ngắn gọn, súc tích để đưa vào một infographic.
    Nội dung bao gồm:
    - Sự kiện chính tại Hà Nội.
    - Hoạt động nổi bật tại TP.HCM và các thành phố lớn.
    - Các hoạt động văn hóa, nghệ thuật trên cả nước.
    - Thông điệp và ý nghĩa chính của ngày lễ.
    """
    infographic_text = generate_text(prompt_content)
    if infographic_text:
        save_text(infographic_text, os.path.join(D3_INFOGRAPHIC_DIR, "noi_dung_infographic.txt"))

    # 2. Sinh hình ảnh nền và các icon/hình minh họa
    prompt_background = "Một background cho infographic về ngày Quốc Khánh Việt Nam. Tông màu chủ đạo là đỏ và vàng. Có hình ảnh cách điệu của hoa sen, sao vàng, và bản đồ Việt Nam. Không có chữ. Phong cách phẳng, tối giản, hiện đại."
    background_image = generate_image(prompt_background, size="1792x1024") # Tỷ lệ ~2:1
    if background_image:
        save_image(background_image, os.path.join(D3_INFOGRAPHIC_DIR, "background.png"))
        
    prompt_icon = "Icon diễu binh, vector, phong cách phẳng, nền trong suốt"
    icon_image = generate_image(prompt_icon, size="1024x1024")
    if icon_image:
        save_image(icon_image, os.path.join(D3_INFOGRAPHIC_DIR, "icon_dieu_binh.png"))
        
    print("--- HOÀN THÀNH WORKFLOW DẠNG ĐỀ 3 ---")
    print(">>> Nhiệm vụ tiếp theo: Dùng Photoshop/Illustrator để ghép nội dung text và các icon lên ảnh nền, tạo thành một infographic hoàn chỉnh.")

def workflow_de_4_website():
    """
    Kịch bản mẫu cho Dạng đề 4: Thiết kế website.
    """
    print("\n--- BẮT ĐẦU WORKFLOW DẠNG ĐỀ 4: WEBSITE ---")

    # 1. Sinh cấu trúc HTML và CSS
    prompt_html = """
    Viết code HTML5 và CSS3 cho một trang web one-page tổng hợp thông tin về sự kiện 80 năm Quốc khánh 2/9.
    Yêu cầu:
    - Giao diện thẩm mỹ, logic, thân thiện, responsive cho desktop và mobile.
    - Có các phần: Header (với logo và menu), Hero Banner, Giới thiệu sự kiện, Lịch trình các hoạt động chính, Thư viện ảnh, Footer.
    - Sử dụng các màu sắc chủ đạo của quốc kỳ Việt Nam.
    - CSS nên được viết trong thẻ <style> bên trong file HTML để dễ dàng quản lý.
    - Sử dụng placeholder cho hình ảnh (ví dụ: 'images/banner.jpg').
    """
    website_code = generate_text(prompt_html, model="gemini-1.5-pro-latest")
    if website_code:
        # Tách code HTML ra khỏi markdown block nếu có
        clean_code = website_code.replace("```html", "").replace("```", "").strip()
        save_text(clean_code, os.path.join(D4_WEBSITE_DIR, "index.html"))

    # 2. Sinh nội dung văn bản cho các mục
    prompt_content = "Viết nội dung giới thiệu ngắn gọn (khoảng 150 từ) cho trang web về ý nghĩa lịch sử của ngày 2/9 và tầm quan trọng của lễ kỷ niệm 80 năm."
    content_text = generate_text(prompt_content)
    if content_text:
        save_text(content_text, os.path.join(D4_WEBSITE_DIR, "content_gioi_thieu.txt"))

    # 3. Sinh hình ảnh cho website
    prompt_banner = "Banner cho website kỷ niệm Quốc khánh Việt Nam, kích thước 1920x600. Hình ảnh Quảng trường Ba Đình và cờ đỏ sao vàng. Không khí trang trọng. Có không gian trống để đặt text. Cinematic."
    banner_image = generate_image(prompt_banner, size="1792x1024") # Chọn size có tỷ lệ gần nhất
    if banner_image:
        save_image(banner_image, os.path.join(D4_WEBSITE_DIR, "images/banner.jpg"))

    print("--- HOÀN THÀNH WORKFLOW DẠNG ĐỀ 4 ---")
    print(">>> Nhiệm vụ tiếp theo: Mở file index.html, điền nội dung từ các file .txt, thay thế placeholder ảnh và triển khai lên web server.")

def workflow_de_5_lyric_song():
    """
    Kịch bản mẫu cho Dạng đề 5: Sáng tác bài hát và video lyric.
    """
    print("\n--- BẮT ĐẦU WORKFLOW DẠNG ĐỀ 5: LYRIC SONG ---")

    # 1. Sáng tác lời bài hát
    prompt_lyrics = """
    Sáng tác lời cho một bài hát (lyric song) về chủ đề 80 năm Quốc khánh 2/9. 
    Lời bài hát cần thể hiện niềm tự hào dân tộc, nhìn lại lịch sử hào hùng và hướng tới tương lai tươi sáng của đất nước.
    Bài hát có cấu trúc: 2 đoạn verse, 1 điệp khúc (lặp lại), 1 đoạn bridge và 1 đoạn outro.
    """
    lyrics = generate_text(prompt_lyrics)
    if lyrics:
        save_text(lyrics, os.path.join(D5_LYRIC_VIDEO_DIR, "loi_bai_hat.txt"))

    # 2. Tạo video nền cho lyric video
    prompt_video_bg = "Video hoạt hình trừu tượng, chuyển động chậm rãi của những dải lụa màu đỏ và vàng trên nền tối. Ánh sáng lấp lánh nhẹ nhàng như những vì sao. Không có nhân vật hay vật thể cụ thể. Phù hợp làm nền cho một video lyric bài hát trang trọng, yêu nước. 4K."
    background_video = generate_video_workflow(prompt_video_bg)
    if background_video:
        save_video(background_video, os.path.join(D5_LYRIC_VIDEO_DIR, "background_video.mp4"))

    print("--- HOÀN THÀNH WORKFLOW DẠNG ĐỀ 5 ---")
    print(">>> Nhiệm vụ tiếp theo: Dùng phần mềm chỉnh sửa video (Adobe Premiere, CapCut) để thêm lời bài hát (từ file .txt) lên video nền, và có thể lồng thêm một bản nhạc không lời phù hợp.")

def workflow_de_6_event_plan():
    """
    Kịch bản mẫu cho Dạng đề 6: Xây dựng kế hoạch sự kiện (PPTX).
    """
    print("\n--- BẮT ĐẦU WORKFLOW DẠNG ĐỀ 6: KẾ HOẠCH SỰ KIỆN ---")

    # 1. Sinh nội dung chi tiết cho từng slide
    prompt_plan = """
    Xây dựng một bản kế hoạch chi tiết cho sự kiện 'Hào Khí Việt Nam - 80 Năm Nhìn Lại' kỷ niệm Quốc khánh 2/9. 
    Bản kế hoạch cần được trình bày dưới dạng nội dung cho các slide PowerPoint, bao gồm:
    - Slide 1: Tên sự kiện, Slogan, Logo ý tưởng.
    - Slide 2: Mục tiêu & Ý nghĩa.
    - Slide 3: Đối tượng tham gia.
    - Slide 4: Timeline tổng thể (Trước, trong, sau sự kiện).
    - Slide 5: Kế hoạch truyền thông.
    - Slide 6: Ý tưởng thiết kế sân khấu, khu vực check-in.
    - Slide 7: Ngân sách dự kiến (các hạng mục chính).
    - Slide 8: Lời kết.
    """
    plan_content = generate_text(prompt_plan)
    if plan_content:
        save_text(plan_content, os.path.join(D6_EVENT_PLAN_DIR, "noi_dung_ke_hoach.txt"))

    # 2. Sinh hình ảnh minh họa cho slide
    prompt_stage_design = "Concept art cho một sân khấu ngoài trời hoành tráng cho sự kiện âm nhạc Quốc Khánh 2/9. Sân khấu có màn hình LED lớn ở giữa hiển thị hình ảnh trống đồng, hai bên là cánh gà cách điệu hình hoa sen. Ánh sáng chủ đạo màu đỏ."
    stage_image = generate_image(prompt_stage_design, size="1792x1024") # Tỷ lệ 16:9 cho slide
    if stage_image:
        save_image(stage_image, os.path.join(D6_EVENT_PLAN_DIR, "thiet_ke_san_khau.png"))
        
    print("--- HOÀN THÀNH WORKFLOW DẠNG ĐỀ 6 ---")
    print(">>> Nhiệm vụ tiếp theo: Mở PowerPoint, tạo các slide và sao chép nội dung từ file .txt, chèn hình ảnh minh họa đã tạo để hoàn thiện file PPTX.")

def workflow_de_7_data_report():
    """
    Kịch bản mẫu cho Dạng đề 7: Xây dựng báo cáo tổng kết từ dữ liệu.
    """
    print("\n--- BẮT ĐẦU WORKFLOW DẠNG ĐỀ 7: BÁO CÁO TỔNG KẾT ---")

    # Dữ liệu mẫu do BTC cung cấp (bạn sẽ thay thế bằng dữ liệu thật)
    sample_data = """
    - Tổng số người tham gia diễu hành tại HN: 50,000 người
    - Lượng khách du lịch đến TP.HCM dịp lễ: 1.2 triệu lượt
    - Số bài báo đưa tin về sự kiện: 5,200 bài
    - Lượng tương tác trên mạng xã hội (tất cả nền tảng): 25 triệu
    - Tỷ lệ phản hồi tích cực: 95%
    """

    # 1. Sinh báo cáo phân tích từ dữ liệu
    prompt_report = f"""
    Dựa trên các số liệu thống kê sau đây về sự kiện kỷ niệm 80 năm Quốc khánh 2/9:
    {sample_data}
    Hãy viết một bản báo cáo tổng kết chuyên nghiệp. Báo cáo cần có các phần:
    1. Tóm tắt tổng quan: Nêu bật những thành công chính.
    2. Phân tích chi tiết: Đi sâu vào từng số liệu và nêu ý nghĩa của chúng.
    3. Đánh giá hiệu quả truyền thông.
    4. Kết luận và đề xuất cho các sự kiện tương lai.
    """
    report_text = generate_text(prompt_report)
    if report_text:
        save_text(report_text, os.path.join(D7_REPORT_DIR, "bao_cao_tong_ket.txt"))

    # 2. Sinh biểu đồ minh họa
    prompt_chart = "Một biểu đồ cột đẹp mắt, chuyên nghiệp để trình bày trong báo cáo. Trục X có các danh mục: 'Người tham gia diễu hành', 'Khách du lịch TP.HCM', 'Tương tác MXH'. Trục Y là số lượng (tính bằng triệu). Phong cách tối giản, màu sắc xanh dương và đỏ."
    chart_image = generate_image(prompt_chart, size="1792x1024")
    if chart_image:
        save_image(chart_image, os.path.join(D7_REPORT_DIR, "bieu_do_minh_hoa.png"))

    print("--- HOÀN THÀNH WORKFLOW DẠNG ĐỀ 7 ---")
    print(">>> Nhiệm vụ tiếp theo: Sử dụng MS Word/Google Docs để định dạng báo cáo từ file .txt và chèn biểu đồ đã tạo.")

def workflow_de_8_mobile_web_game():
    """
    Kịch bản mẫu cho Dạng đề 8: Xây dựng game mobile web.
    """
    print("\n--- BẮT ĐẦU WORKFLOW DẠNG ĐỀ 8: GAME ---")

    # 1. Sinh code game (HTML, CSS, JS)
    prompt_game_code = """
    Viết code cho một game mobile web đơn giản tên là 'Hành Trình Lịch Sử' dưới dạng một file HTML duy nhất (bao gồm cả CSS và JavaScript).
    - Ý tưởng game: Một game trắc nghiệm kiến thức về lịch sử ngày 2/9.
    - Giao diện: Responsive, hiển thị tốt trên điện thoại.
    - Gameplay: Hiện ra câu hỏi và 4 đáp án. Người chơi chọn đáp án đúng để sang câu tiếp theo. Có tính điểm.
    - Dữ liệu câu hỏi: Tạo sẵn 5 câu hỏi mẫu trong code JS.
    """
    game_code = generate_text(prompt_game_code, model="gemini-1.5-pro-latest")
    if game_code:
        clean_code = game_code.replace("```html", "").replace("```", "").strip()
        save_text(clean_code, os.path.join(D8_GAME_DIR, "game.html"))

    # 2. Sinh tài sản đồ họa cho game
    prompt_background = "Background cho một game mobile về lịch sử Việt Nam. Hình ảnh làng quê Việt Nam với cây đa, mái đình, được vẽ theo phong cách hoạt hình 2D, màu sắc tươi sáng."
    bg_image = generate_image(prompt_background, size="1024x1792") # Tỷ lệ màn hình điện thoại
    if bg_image:
        save_image(bg_image, os.path.join(D8_GAME_DIR, "assets/background.png"))
        
    prompt_button = "Nút bấm (button) cho game mobile, hình chữ nhật bo góc, màu đỏ, có viền vàng, hiệu ứng 3D nổi khối đơn giản."
    btn_image = generate_image(prompt_button, size="1024x1024")
    if btn_image:
        save_image(btn_image, os.path.join(D8_GAME_DIR, "assets/button.png"))
        
    print("--- HOÀN THÀNH WORKFLOW DẠNG ĐỀ 8 ---")
    print(">>> Nhiệm vụ tiếp theo: Chỉnh sửa file game.html để liên kết đến các file ảnh trong thư mục assets và triển khai lên web server.")

def workflow_de_9_flyer():
    """
    Kịch bản mẫu cho Dạng đề 9: Thiết kế tờ gấp (flyer) A4 gấp ba.
    """
    print("\n--- BẮT ĐẦU WORKFLOW DẠNG ĐỀ 9: FLYER ---")

    # 1. Sinh nội dung text cho flyer
    prompt_flyer_text = """
    Viết nội dung cho một tờ gấp A4 tuyên truyền về ngày 2/9. Nội dung cần cực kỳ ngắn gọn, hấp dẫn, chia thành 3 phần chính tương ứng với 3 mặt của tờ gấp:
    - Mặt 1 (Gấp vào trong): Lịch sử và ý nghĩa của ngày 2/9.
    - Mặt 2 (Ở giữa): Các hoạt động chính trong dịp kỷ niệm 80 năm.
    - Mặt 3 (Bìa khi gấp lại): Tiêu đề lớn 'Mừng Quốc Khánh 2/9', hình ảnh biểu trưng, và thông điệp kêu gọi.
    """
    flyer_text = generate_text(prompt_flyer_text)
    if flyer_text:
        save_text(flyer_text, os.path.join(D9_FLYER_DIR, "noi_dung_flyer.txt"))

    # 2. Sinh thiết kế hoàn chỉnh cho flyer
    prompt_flyer_design = """
    Thiết kế một tờ flyer A4 nằm ngang để gấp ba, chủ đề Quốc Khánh Việt Nam.
    - Bố cục chia thành 3 phần rõ rệt.
    - Phần bên phải (sẽ là trang bìa khi gấp): Nền đỏ, ở giữa là hình sao vàng lớn cách điệu, bên dưới là dòng chữ 'Mừng 80 Năm Quốc Khánh 2/9'.
    - Phần ở giữa: Nền trắng, có các placeholder để điền text về lịch trình sự kiện. Có hình ảnh minh họa nhỏ về diễu binh.
    - Phần bên trái: Nền trắng, có placeholder cho text lịch sử và hình ảnh Bác Hồ đọc Tuyên ngôn Độc lập.
    - Phong cách thiết kế hiện đại, trang trọng.
    """
    # Kích thước A4 ngang ~ 29.7 x 21 cm (tỷ lệ ~1.4:1). Chọn size gần nhất.
    flyer_design = generate_image(prompt_flyer_design, size="1792x1024")
    if flyer_design:
        save_image(flyer_design, os.path.join(D9_FLYER_DIR, "thiet_ke_flyer.jpg"))

    print("--- HOÀN THÀNH WORKFLOW DẠNG ĐỀ 9 ---")
    print(">>> Nhiệm vụ tiếp theo: Dùng Photoshop để thêm/chỉnh sửa nội dung text từ file .txt vào file ảnh thiết kế, sau đó xuất ra file PDF/JPG chất lượng cao để in ấn.")

# ==============================================================================
# ==                            ĐIỂM BẮT ĐẦU CHẠY                             ==
# ==============================================================================
if __name__ == "__main__":
    # KIỂM TRA CHI PHÍ TRƯỚC KHI CHẠY
    check_api_spend()

    # --- HÃY CHỌN 1 TRONG CÁC WORKFLOW DƯỚI ĐÂY ĐỂ CHẠY ---
    # Bỏ comment (xóa dấu #) ở dòng tương ứng với đề thi của bạn.
    
    # workflow_de_1_video_ban_tin()
    # workflow_de_2_truyen_tranh()
    # workflow_de_3_infographic()
    # workflow_de_4_website()
    workflow_de_5_lyric_song()
    # workflow_de_6_event_plan()
    # workflow_de_7_data_report()
    # workflow_de_8_mobile_web_game()
    # workflow_de_9_flyer()

    print("\n\n🎉 Tất cả các tác vụ đã chọn đã chạy xong! Hãy kiểm tra thư mục 'final_product'.")
    # KIỂM TRA CHI PHÍ SAU KHI CHẠY
    check_api_spend()