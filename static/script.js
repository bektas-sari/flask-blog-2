document.addEventListener("DOMContentLoaded", function () {
    // Sosyal Medya Paylaşım Butonları
    document.querySelectorAll(".social-share a").forEach((button) => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Varsayılan davranışı engelle
            let shareUrl = this.getAttribute("data-url"); // Butondaki URL'yi al
            window.open(shareUrl, "_blank", "width=600,height=500"); // Yeni pencerede aç
        });
    });
});
