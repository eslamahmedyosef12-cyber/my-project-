python app.py
ls -R
cd aboqalas_site
python app.py
nano app.py
nano index.html
python app.py
ls ~/aboqalas_site/templates/
cd templates
nano thankyou.html
python app.py
cd ..
python app.py
mkdir -p static
mv 1000222673.jpg static/bg.jpg
ls
cd ~
find /sdcard -name "1000222673.jpg"
termux-setup-storage
find /sdcard -name "1000222673.jpg"
find ~/storage/shared/DCIM -name "1000222673.jpg"
find ~/storage/shared/Download -name "1000222673.jpg"
cp /sdcard/Download/1000222673.jpg ~/aboqalas_site/static/bg.jpg
ls ~/storage/shared/Download
ls ~/storage/shared/DCIM/Camera
ls -lt ~/storage/shared/DCIM/Camera | head -n 20
cp $(ls -t ~/storage/shared/DCIM/Camera/*.jpg | head -n 1) ~/aboqalas_site/static/bg.jpg
cp /sdcard/Download/1000222673.jpg ~/aboqalas_site/static/bg.jpg
cd templates
nano thankyou.html
cd aboqalas_site
python app.py
cd aboqalas_site
cd ..
# 1. تأكد إن Flask مثبت
pip install flask
# 2. شغّل الملف
python pentest_lab.py
# 3. افتح المتصفح
http://127.0.0.1:5000
pip install flask
nano filename.py
pentest_lab.py
python app.py
cd my_first_app
flutter build apk
flutter clean
flutter pub cache repair
flutter build apk
echo "==== 1. فحص Flutter ===="
flutter --version
echo ""
echo "==== 2. فحص doctor ===="
flutter doctor
echo ""
echo "==== 3. فحص Android SDK ===="
echo $ANDROID_HOME
ls $ANDROID_HOME 2>/dev/null || echo "ANDROID_HOME مش متظبط"
echo ""
echo "==== 4. فحص Java ===="
java -version
echo ""
echo "==== 5. مساحة التخزين ===="
pkg update && pkg upgrade
flutter doctor
