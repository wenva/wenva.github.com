# 牛逼的ImageMagick

ImageMagick[1] 是一个免费的创建、编辑、合成图片的软件。可用于格式转换、变换、透明度设置、特效....; 可支持的格式多达89种。

## 小试牛刀
若你想将jpg文件转换成bmp、png、psd..., 只有执行如下动作:
<pre>
convert x.jpg x.bmp
</pre>

PS：以前无法是图片转个格式，变个大小，统统都开启PS，现在突然发现酱紫弱爆了
<pre>
下ImageMagick支持至少90种图片格式: A, ART, AVI, AVS, B, BIE, BMP, BMP2, BMP3, C, CACHE, CAPTION, CIN, CIP, CLIP, CLIPBOARD, CMYK, CMYKA, CUR, CUT, DCM, DCX, DNG, DOT, DPS, DPX, EMF, EPDF, EPI, EPS, EPS2, EPS3, EPSF, EPSI, EPT, EPT2, EPT3, FAX, FITS, FPX, FRACTAL, G, G3, GIF, GIF87, GRADIENT, GRAY, HDF, HISTOGRAM, HTM, HTML, ICB, ICO, ICON, JBG, JBIG, JNG, JP2, JPC, JPEG, JPG, JPX, K, LABEL, M, M2V, MAP, MAT, MATTE, MIFF, MNG, MONO, MPC, MPEG, MPG, MSL, MTV, MVG, NULL, O,OTB, P7, PAL, PALM, PATTERN, PBM, PCD, PCDS, PCL, PCT, PCX, PDB, PDF, PFA, PFB, PGM, PGX, PICON, PICT, PIX, PJPEG, PLASMA, PNG, PNG24, PNG32, PNG8, PNM, PPM, PREVIEW, PS, PS2, PS3, PSD, PTIF, PWP, R, RAS, RGB, RGBA, RGBO, RLA, RLE, SCR, SCT, SFW, SGI, SHTML, STEGANO, SUN, SVG, SVGZ, TEXT, TGA, TIF, TIFF, TILE, TIM, TTC, TTF, TXT, UIL, UYVY, VDA, VICAR, VID, VIFF, VST, WBMP, WMF, WMFWIN32, WMZ, WPG, X, XBM, XC, XCF, XPM, XV, XWD, Y, YCbCr, YCbCrA, YUV
</pre>

## 安装
这么好用的工具果断装起，安装方法也so easy.
<pre>
sudo brew install ImageMagick
</pre>

## [使用](http://www.imagemagick.org/script/command-line-options.php)
###### 1. 转换格式
<pre>
convert x.jpg x.bmp
</pre>

###### 2. 透明
JPG图象是不含有透明通道的，PNG TIG TIG GIF等是具有透明通道的
<pre>
convert -alpha type x.png x1.png
</pre>

常用type
<pre>
Opaque - 不透
Transparent - 透明
</pre>

