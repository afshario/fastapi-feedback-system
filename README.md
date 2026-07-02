# سیستم فیدبک (Feedback System)

یک سیستم مدیریت فیدبک کامل و مدرن توسعه یافته با **FastAPI**.

---

## ✨ ویژگی‌ها

- ثبت‌نام و ورود کاربران با JWT
- ایجاد، مشاهده، ویرایش و حذف فیدبک
- سیستم رای‌گیری (لایک و دیسلایک)
- امکان ثبت کامنت برای هر فیدبک
- داشبورد ادمین برای پاسخ به فیدبک‌ها
- پشتیبانی کامل از Docker و Docker Compose

---

## 🛠️ تکنولوژی‌ها

- **Backend**: FastAPI + SQLAlchemy
- **Database**: MySQL 8.0
- **Authentication**: JWT + Passlib (bcrypt)
- **Frontend**: Jinja2 Templates + Tailwind CSS
- **Container**: Docker + Docker Compose

---

## 🚀 نحوه اجرا

### 1. کلون کردن پروژه
```bash
git clone https://github.com/afshario/fastapi-feedback-system
cd fastapi-feedback-system

```

### 2. ساخت فایل .env
### 3. اجرا با docker-compose
```bash
docker-compose up --build
```
 پس از اجرا اپلیکیشن در آدرس زیر در دسترس میباشد
 ```bash
 http://localhost:8000
```
