import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Derivative Analysis Model",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS (Academic style)
# =========================
st.markdown("""
<style>
    h1 {
        font-size: 2.1rem !important;
        font-weight: 600 !important;
        font-family: 'Times New Roman', Times, serif;
        color: #2c3e50;
        margin-bottom: 0.4rem !important;
    }
    h2, h3, h4 {
        font-family: 'Times New Roman', Times, serif;
        color: #34495e;
    }
    .stApp { background-color: #ffffff; }

    /* Sidebar title styling */
    .sidebar-title {
        font-family: 'Times New Roman', Times, serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #2c3e50;
        line-height: 1.25;
        margin-bottom: 0.75rem;
    }

    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 6px;
    }

    /* LaTeX-friendly academic box via blockquote */
    blockquote {
        padding: 18px;
        border-radius: 6px;
        background-color: #f8f9fa;
        border-left: 4px solid #2c3e50;
        margin: 0 0 18px 0;
        font-family: 'Georgia', serif;
        color: #212529;
        line-height: 1.65;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Helpers
# =========================
def academic_box_md(text: str):
    st.markdown("> " + text.replace("\n", "\n> "))

def to_sympy_x0(x0):
    try:
        return sp.nsimplify(x0)
    except Exception:
        return sp.Rational(str(x0))

def algebraic_derivative(func, x0):
    """
    Computes tangent slope k at x0 using the algebraic criterion:
    f(x) - (f(x0) + k(x-x0)) has no linear term near x0.
    """
    x, k = sp.symbols('x k')
    x0_sym = to_sympy_x0(x0)

    try:
        f = sp.sympify(func) if isinstance(func, str) else func
        f_x0 = sp.simplify(f.subs(x, x0_sym))
        diff = sp.simplify(f - (f_x0 + k * (x - x0_sym)))

        series = sp.series(diff, x, x0_sym, n=3).removeO()
        linear_term = sp.expand(series).coeff(x - x0_sym)

        sol = sp.solve(sp.Eq(linear_term, 0), k)
        if not sol:
            return None, None, "k not found"

        k_val = sp.simplify(sol[0])
        tangent_eq = sp.simplify(f_x0 + k_val * (x - x0_sym))
        return f, k_val, tangent_eq

    except Exception as e:
        return None, None, str(e)

def solve_kapanadze_3d(func_str, x0_val, y0_val):
    x, y = sp.symbols('x y')
    try:
        func = sp.sympify(func_str)
        x0s, y0s = to_sympy_x0(x0_val), to_sympy_x0(y0_val)
        z0 = sp.simplify(func.subs({x: x0s, y: y0s}))
        kx_val = sp.simplify(sp.diff(func, x).subs({x: x0s, y: y0s}))
        ky_val = sp.simplify(sp.diff(func, y).subs({x: x0s, y: y0s}))
        return func, kx_val, ky_val, z0
    except Exception as e:
        return None, None, None, str(e)

# =========================
# Numeric formatting (removes 1.00 -> 1)
# =========================
FMT = "%.6g"

# =========================
# Translations (full academic text, no bullets, no I/II/III)
# =========================
translations = {
    "KA": {
        "lang_label": "### 🌐 Language / ენა",
        "lang_ka": "ქართული",
        "lang_en": "English",

        "main_title": "ინტერაქტიული კომპიუტერული მოდელი წარმოებულის გეომეტრიული და ალგებრული ინტერპრეტაციისათვის",

        "nav_label": "ნავიგაცია",
        "nav_options": [
            "შემხები წრფის გეომეტრიული წარმოშობა",
            "ალგებრული კრიტერიუმი",
            "სივრცითი განზოგადება",
            "ტრიგონომეტრიული ფუნქციები",
            "მაჩვენებლიანი და ლოგარითმული ფუნქციები",
            "კავშირი კლასიკურ ანალიზთან",
            "მეთოდის გამოყენების საზღვრები",
        ],

        # Common sublabels
        "sub_context": "კონტექსტი",
        "sub_inputs": "საწყისი მონაცემები",
        "sub_interpretation": "ინტერპრეტაცია",
        "sub_results": "შედეგები",
        "sub_editorial": "რედაქციული შენიშვნები (რა შეიცვალა და რატომ)",

        # Section 1
        "s1_title": "მკვეთი წრფის თანმიმდევრული მიახლოება შემხებ წრფასთან",
        "s1_text": (
            "შემხები წრფე განიხილება, როგორც მკვეთი წრფის **ზღვრული შემთხვევა**, როდესაც "
            "მოძრავი წერტილი თანმიმდევრულად უახლოვდება ფუნქციის გრაფიკზე ფიქსირებულ წერტილს."
        ),
        "s1_label_func": "განხილული ფუნქცია",
        "s1_label_fixed": "ფიქსირებული წერტილი",
        "s1_label_param": "მეორე წერტილის პარამეტრი",
        "s1_label_increment": "არგუმენტის ნაზრდი",
        "s1_editorial": (
            "„ლიმიტური შემთხვევა“ ჩანაცვლებულია „ზღვრული შემთხვევით“, როგორც უფრო სტანდარტული აკადემიური ტერმინით.\n\n"
            "„მეორე წერტილი“ ჩანაცვლებულია „მოძრავი წერტილით“ მათემატიკური სიზუსტისთვის.\n\n"
            "„მეორე წერტილის დაშორება“ გადმოტანილია „არგუმენტის ნაზრდის“ ენაზე, რადგან ეს ტერმინი უკეთ ეთანხმება ნაზრდი/დიფერენციალი/ნაშთის ხაზს."
        ),
        "secant": "მკვეთი წრფე",
        "tangent": "შემხები წრფე",
        "viz_title": "გეომეტრიული ვიზუალიზაცია",

        # Section 2
        "s2_title": "ნაშთის კვადრატზე გაყოფის ალგებრული მეთოდი",
        "s2_thm_title": "ალგებრული კრიტერიუმი შემხები წრფისათვის",
        "s2_thm_text": (
            "წრფე $y = k(x-x_0) + f(x_0)$ არის ფუნქციის $f(x)$ შემხები წრფე წერტილში $x_0$ "
            "მაშინ და მხოლოდ მაშინ, როდესაც ფუნქციისა და აღნიშნული წრფის სხვაობა იყოფა $(x-x_0)^2$-ზე.\n\n"
            "ანუ, არსებობს ისეთი ფუნქცია $\\varphi(x)$, რომ\n\n"
            "$$f(x) - \\big(k(x-x_0) + f(x_0)\\big) = (x-x_0)^2\\,\\varphi(x).$$"
        ),
        "s2_interp": (
            "ეს პირობა ნიშნავს, რომ ფუნქციისა და მისი შემხები წრფის სხვაობა $x_0$-ის მახლობლად წარმოადგენს "
            "**მეორე რიგის უსასრულოდ მცირე სიდიდეს**; შესაბამისად, ნაშთი ლოკალურად ქრება უფრო სწრაფად, ვიდრე პირველი რიგის სიდიდეები, "
            "რაც უზრუნველყოფს შემხები წრფის არსებობასა და უნიკალურობას."
        ),
        "s2_label_func": "განხილული ფუნქცია",
        "s2_label_x0": "შეხების წერტილი",
        "btn_analyze": "გამოთვლა და ანალიზი",
        "s2_res_slope": "დახრილობის კოეფიციენტი",
        "s2_res_eq": "შემხები წრფის განტოლება",
        "s2_ok": (
            "ნაშთი აკმაყოფილებს ალგებრულ კრიტერიუმს და წარმოადგენს მეორე რიგის უსასრულოდ მცირე სიდიდეს, "
            "რის შედეგადაც შემხები წრფის არსებობა დადასტურებულია."
        ),
        "s2_fail": "კრიტერიუმის ანალიზი ვერ შესრულდა (შეყვანის/ფორმულის პრობლემა).",
        "proof_title": "ნაშთის ანალიზი",
        "vis_touch": "ფუნქცია და შემხები",
        "residue": "ნაშთი",

        "s2_editorial": (
            "ამოღებულია ემოციური ნიშანი და არაზუსტი ფორმულირება „სასრული“.\n\n"
            "„მეორე რიგის მცირე“ ჩანაცვლებულია მკაცრი ანალიზური ფორმით: „მეორე რიგის უსასრულოდ მცირე სიდიდე“.\n\n"
            "განმეორებითი ფრაზები და არასაჭირო გამეორებები დაყვანილია ერთიან, აკადემიურ სტილზე."
        ),

        # Section 3
        "s3_title": "კაპანაძის მიდგომის სივრცითი განზოგადება",
        "s3_text": (
            "ერთგანზომილებიანი შემთხვევის ანალოგიურად, სამგანზომილებიან სივრცეში განიხილება ზედაპირი $z=f(x,y)$ "
            "და შემხები წრფის ნაცვლად განისაზღვრება **შემხები სიბრტყე** წერტილში $(x_0,y_0)$. "
            "შემხები სიბრტყე განისაზღვრება იმ პირობით, რომ ზედაპირსა და შესაბამის სიბრტყეს შორის სხვაობა აღნიშნული წერტილის მახლობლად "
            "წარმოადგენს მეორე რიგის უსასრულოდ მცირე სიდიდეს. ეს კრიტერიუმი უზრუნველყოფს არსებობასა და უნიკალურობას და იძლევა "
            "დიფერენციალური გეომეტრიის ბუნებრივ ინტერპრეტაციას ზღვრის ცნების უშუალო გამოყენების გარეშე საწყის ეტაპზე."
        ),
        "s3_label_surface": "განხილული ზედაპირი",
        "s3_label_point": "შეხების წერტილი",
        "s3_coeffs": "დახრილობის კოეფიციენტები",
        "s3_conc": (
            "ეს ნიშნავს, რომ მოცემულ წერტილში შემხები სიბრტყე წარმოადგენს ზედაპირის ლოკალურ ლინეურ მიახლოებას."
        ),
        "build_3d": "3D მოდელის აგება",
        "surface": "ზედაპირი",
        "tan_plane": "შემხები სიბრტყე",
        "s3_editorial": (
            "„ტოპოლოგიური“ ჩანაცვლებულია „სივრცითი“-ით, რადგან აქ ფოკუსი დიფერენციალურ გეომეტრიაზეა.\n\n"
            "დამატებულია არსებობა/უნიკალურობა და „ლინეური მიახლოება“ კონცეპტუალური სიზუსტისთვის.\n\n"
            "ამოღებულია ზედმეტი გამეორებები."
        ),

        # Section 4
        "s4_title": "ტრიგონომეტრიული ფუნქციების გეომეტრიულ–ალგებრული ანალიზი",
        "s4_text": (
            "მოდელი ეფუძნება ტრიგონომეტრიული ფუნქციების წარმოებულების გეომეტრიულ და ალგებრულ ინტერპრეტაციას. "
            "ანალიზი ხორციელდება ერთეულოვან წრეწირზე წერტილის მოძრაობის მოდელის გამოყენებით, რაც უზრუნველყოფს "
            "კუთხესა და შესაბამის ფუნქციურ მნიშვნელობებს შორის დამოკიდებულების გეომეტრიულ გააზრებას.\n\n"
            "ერთეულოვან წრეწირზე მოძრაობისას სინუსისა და კოსინუსის ფუნქციები განიხილება როგორც კოორდინატული პროექციები, "
            "ხოლო კოსინუსის მნიშვნელობა ინტერპრეტირდება როგორც სინუსის შესაბამისი შემხები წრფის დახრილობის კოეფიციენტი. "
            "ამგვარად, ერთეულოვანი წრეწირი, ფუნქციის ცვლილების სიჩქარე და წარმოებულის ცნება ერთ კონცეპტუალურ ჩარჩოში ერთიანდება."
        ),
        "trig_mode_select": "ვიზუალიზაციის რეჟიმი",
        "trig_standard": "ტრიგონომეტრიული წრეწირი (sin, cos)",
        "trig_inverse": "შებრუნებული ტრიგონომეტრიული ფუნქციები",
        "unit_circle": "ერთეულოვანი წრეწირი",
        "inv_info": (
            "მოცემული ფუნქციური მნიშვნელობიდან განისაზღვრება შესაბამისი კუთხე განსაზღვრულ არეებში, "
            "რაც ასახავს კუთხესა და მნიშვნელობას შორის ერთმნიშვნელოვან დამოკიდებულებას."
        ),
        "inv_res": "შედეგები (კუთხეები)",
        "s4_conc": (
            "წარმოდგენილი კონსტრუქცია უზრუნველყოფს წარმოებულის ცნების კონცეპტუალურ გააზრებას მოძრაობის, დახრილობისა და ფუნქციური დამოკიდებულების საფუძველზე."
        ),
        "s4_editorial": (
            "ამოღებულია განმეორებითი ფრაზები და ზედმეტი განმარტებები.\n\n"
            "„სიჩქარე“ ჩანაცვლებულია „ცვლილების სიჩქარით“ და „დახრილობის კოეფიციენტით“, როგორც უფრო ზუსტი ანალიზური ტერმინებით."
        ),

        # Section 5
        "s5_title": "მაჩვენებლიანი და ლოგარითმული ფუნქციების გეომეტრიულ–ალგებრული ანალიზი",
        "s5_text": (
            "მოცემულ ნაწილში განიხილება მაჩვენებლიანი და ლოგარითმული ფუნქციები გეომეტრიულ–ალგებრული მიდგომის ფარგლებში. "
            "ანალიზი ეფუძნება შემხები წრფის ალგებრულ კრიტერიუმს და ფუნქციის ლოკალური ლინეური მიახლოების იდეას."
        ),
        "s5_select_mode": "ფუნქციის ტიპი",
        "exp_mode": "მაჩვენებლიანი ფუნქცია ($e^x$)",
        "log_mode": "ლოგარითმული ფუნქცია ($\\log_a x$)",
        "s5_exp_info": (
            "მაჩვენებლიანი ფუნქცია ხასიათდება იმ თვისებით, რომ მისი წარმოებული ყველა წერტილში ემთხვევა თავად ფუნქციის მნიშვნელობას:\n\n"
            "$$\\frac{d}{dx}e^x = e^x.$$"
        ),
        "s5_log_info": (
            "ლოგარითმული ფუნქციის წარმოებული განისაზღვრება ფორმულით:\n\n"
            "$$\\frac{d}{dx}\\log_a(x)=\\frac{1}{x\\ln(a)}.$$"
        ),
        "bases": ["e (ნატურალური)", "10 (ათობითი)", "2 (ორობითი)"],
        "base_select": "ფუძის არჩევა",
        "calc_log": "ანალიზი",
        "value_eq_slope": "მოცემულ წერტილში ფუნქციის მნიშვნელობა და შესაბამისი შემხები წრფის დახრილობის კოეფიციენტი ერთმანეთს ემთხვევა.",
        "s5_conc": (
            "მაჩვენებლიანი და ლოგარითმული ფუნქციების ეს ანალიზი აჩვენებს, რომ წარმოებული ინტერპრეტირდება როგორც ლოკალური ლინეური მიახლოების დახრილობა და ქმნის ბუნებრივ კავშირს გეომეტრიულ ინტუიციასა და ფორმალურ ანალიზს შორის."
        ),
        "s5_editorial": (
            "ამოღებულია ტექსტის განმეორებები და არაზუსტი ფორმები.\n\n"
            "სტრუქტურა გამკაცრებულია: ჯერ მაჩვენებლიანი, შემდეგ ლოგარითმული.\n\n"
            "„დახრის კოეფიციენტი“ ჩანაცვლებულია სწორი ფორმით: „დახრილობის კოეფიციენტი“."
        ),

        # Section 6
        "s6_title": "კავშირი ნიუტონისა და კოშის კლასიკურ მიდგომებთან",
        "s6_text": (
            "მოცემულ ნაწილში განიხილება გეომეტრიულ–ალგებრული მიდგომის კავშირი ნიუტონისა და კოშის კლასიკურ კონცეფციებთან. "
            "მეთოდი არ ეწინააღმდეგება კლასიკურ ანალიზს; იგი წარმოადგენს didactic გზას იმავე თეორიულ შედეგებამდე მისასვლელად.\n\n"
            "მიდგომაში წარმოებული თავდაპირველად განიხილება როგორც ზღვრული გეომეტრიული ობიექტი — ფუნქციის გრაფიკზე აგებული შემხები წრფე, "
            "რომელიც მიიღება ალგებრული კრიტერიუმის შესრულების შედეგად და შემდგომ იღებს ანალიტიკურ ფორმალიზაციას."
        ),
        "x0_label": "ფიქსირებული წერტილი $x_0$",
        "dx_label": "არგუმენტის ნაზრდი $\\Delta x$",
        "delta_f": "ფუნქციის ნაზრდი $\\Delta F$",
        "d_f": "დიფერენციალი $dF$",
        "diff_val": "ნაშთი $\\Delta F - dF$",
        "kapanadze_limit_text": (
            "თუ $\\Delta F - dF$ არის მეორე რიგის უსასრულოდ მცირე, ალგებრული კრიტერიუმი შესრულებულია და დახრილობა განსაზღვრავს წარმოებულს."
        ),
        "phys_header": "ფიზიკური ინტერპრეტაცია (კინემატიკა)",
        "phys_info": (
            "ფიზიკურ კონტექსტში წარმოებული ინტერპრეტირდება როგორც სხეულის მომენტალური სიჩქარე; ტრაექტორიაზე აგებული შემხები ასახავს მომენტალურ მიმართულებას ინერციული პრინციპის შესაბამისად."
        ),
        "time": "დრო $t$",
        "velocity_vec": "მომენტალური სიჩქარის ვექტორი",
        "trajectory": "ტრაექტორია",
        "body": "სხეული",
        "inertia": "ინერციული მიმართულება (შემხები)",
        "ground": "ზედაპირი",
        "ballistic": "ბალისტიკური მოძრაობის მოდელი",
        "s6_editorial": (
            "ამოღებულია საუბრული ფორმულირებები და ზედმეტი განმეორებები.\n\n"
            "ტერმინოლოგია ერთიანდება: ნაზრდი / დიფერენციალი / ნაშთი.\n\n"
            "ფიზიკური ნაწილი გადაყვანილია კლასიკური მექანიკის აკადემიურ ენაზე."
        ),

        # Section 7
        "s7_title": "მეთოდის გამოყენების საზღვრები (განსაკუთრებული შემთხვევები)",
        "s7_text": (
            "განიხილება ისეთი ფუნქციები, რომელთა შემთხვევაში ნაშთის კვადრატზე გაყოფის ალგებრული კრიტერიუმი ავლენს წარმოებულის არარსებობას "
            "და ამით განსაზღვრავს მეთოდის გამოყენების საზღვრებს."
        ),
        "select_case": "აირჩიეთ შემთხვევა",
        "case_options": ["|x| (მოდული 0-ში)", "|x|^1.5 (ნაკლები სიგლუვე)", "x^2·sin(1/x) (ოსცილაცია)"],
        "case_abs_text": (
            "ფუნქციისთვის $f(x)=|x|$ წერტილში $x=0$ არსებობს ორი განსხვავებული ცალმხრივი დახრილობა: "
            "მარცხნიდან $k=-1$, მარჯვნიდან $k=1$. შედეგად, შემხები წრფის უნიკალურობა ირღვევა."
        ),
        "case_1_text": (
            "შემთხვევაში $f(x)=|x|^{1.5}$ წარმოებულის საკითხი დაკავშირებულია ნაშთის ქცევის სტაბილურობასთან; "
            "მოდელი აჩვენებს, რომ კრიტერიუმის შესრულება შეიძლება პრობლემური იყოს ლოკალური ქცევის გამო."
        ),
        "case_2_text": (
            "ფუნქცია $x^2\\sin(1/x)$ (0-ის მახლობლად) ირხევა სწრაფად; ნაშთი შეიძლება არ სტაბილურდებოდეს, რაც უშლის ხელს კრიტერიუმის დაკმაყოფილებას."
        ),
        "conclusion": "დასკვნა: ამ შემთხვევაში წარმოებული არ არსებობს.",
        "left_tan": "მარცხენა შემხები",
        "right_tan": "მარჯვენა შემხები",
        "s7_editorial": (
            "დამატებულია „ცალმხრივი დახრილობა“ და „ლინეური მიახლოება“ კონცეპტუალური სიცხადისთვის.\n\n"
            "ალგებრული განმარტება გამკაცრებულია (მეორე რიგის უსასრულოდ მცირე)."
        ),
    },

    "EN": {
        "lang_label": "### 🌐 Language / ენა",
        "lang_ka": "ქართული",
        "lang_en": "English",

        "main_title": "Interactive Computational Model for the Geometric and Algebraic Interpretation of the Derivative",

        "nav_label": "Navigation",
        "nav_options": [
            "Geometric origin of the tangent",
            "Algebraic criterion",
            "Spatial generalization",
            "Trigonometric functions",
            "Exponential and logarithmic functions",
            "Connection with classical analysis",
            "Limits of applicability",
        ],

        "sub_context": "Context",
        "sub_inputs": "Inputs",
        "sub_interpretation": "Interpretation",
        "sub_results": "Results",
        "sub_editorial": "Editorial notes (what changed and why)",

        "s1_title": "Successive approximation of the secant to the tangent",
        "s1_text": (
            "The tangent line is treated as the **limiting case** of a secant line, "
            "when a moving point approaches a fixed point on the graph of the function."
        ),
        "s1_label_func": "Function under consideration",
        "s1_label_fixed": "Fixed point",
        "s1_label_param": "Second-point parameter",
        "s1_label_increment": "Argument increment",
        "s1_editorial": (
            "“Limiting case” is phrased in a more standard academic form (Georgian: “ზღვრული შემთხვევა”).\n\n"
            "“Second point” is refined to “moving point” for mathematical precision.\n\n"
            "Distance-based phrasing is aligned with the increment language (Δx), consistent with the increment/differential/remainder framework."
        ),
        "secant": "Secant line",
        "tangent": "Tangent line",
        "viz_title": "Geometric visualization",

        "s2_title": "Algebraic method: divisibility of the remainder by the square",
        "s2_thm_title": "Algebraic criterion for a tangent line",
        "s2_thm_text": (
            "The line $y = k(x-x_0) + f(x_0)$ is tangent to $f(x)$ at $x_0$ iff\n\n"
            "$$f(x) - \\big(k(x-x_0) + f(x_0)\\big) = (x-x_0)^2\\,\\varphi(x).$$"
        ),
        "s2_interp": (
            "This means that the difference between the function and its tangent line near $x_0$ is a **second-order infinitesimal**, "
            "which ensures existence and uniqueness of the tangent in a local sense."
        ),
        "s2_label_func": "Function under consideration",
        "s2_label_x0": "Point of tangency",
        "btn_analyze": "Compute and analyze",
        "s2_res_slope": "Slope coefficient",
        "s2_res_eq": "Equation of the tangent line",
        "s2_ok": (
            "The remainder satisfies the algebraic criterion and behaves as a second-order infinitesimal; the tangent line is therefore confirmed."
        ),
        "s2_fail": "The analysis could not be completed (input/formula issue).",
        "proof_title": "Remainder analysis",
        "vis_touch": "Function and tangent",
        "residue": "Remainder",
        "s2_editorial": (
            "Removed emotive markers and imprecise phrasing.\n\n"
            "Replaced “second-order small” with the strict analytic expression “second-order infinitesimal”.\n\n"
            "Unified notation and reduced redundant repetition."
        ),

        "s3_title": "Spatial generalization of the approach",
        "s3_text": (
            "In analogy with the one-dimensional case, consider a surface $z=f(x,y)$ in 3D. "
            "Instead of a tangent line, we define a **tangent plane** at $(x_0,y_0)$. "
            "The plane is characterized by the requirement that the surface–plane difference near the point is a "
            "second-order infinitesimal. This yields existence/uniqueness and provides a natural differential-geometric interpretation."
        ),
        "s3_label_surface": "Surface under consideration",
        "s3_label_point": "Point of tangency",
        "s3_coeffs": "Slope coefficients",
        "s3_conc": "Thus, the tangent plane provides a local linear approximation of the surface.",
        "build_3d": "Build 3D model",
        "surface": "Surface",
        "tan_plane": "Tangent plane",
        "s3_editorial": (
            "Replaced “topological” wording with “spatial” as the focus is differential geometry.\n\n"
            "Added explicit existence/uniqueness and local linear approximation.\n\n"
            "Removed redundant technical repetition."
        ),

        "s4_title": "Geometric–algebraic analysis of trigonometric functions",
        "s4_text": (
            "The model provides geometric and algebraic interpretations of trigonometric derivatives. "
            "It is based on motion on the unit circle, making the relation between angles and function values conceptually transparent.\n\n"
            "On the unit circle, sine and cosine are treated as coordinate projections; the cosine value can be interpreted as the slope of the tangent line to the sine curve at the corresponding point."
        ),
        "trig_mode_select": "Visualization mode",
        "trig_standard": "Unit circle (sin, cos)",
        "trig_inverse": "Inverse trigonometric functions",
        "unit_circle": "Unit circle",
        "inv_info": (
            "Given a function value, the corresponding angle is determined on the appropriate domain, reflecting one-to-one dependence in those ranges."
        ),
        "inv_res": "Results (angles)",
        "s4_conc": (
            "This construction supports conceptual understanding of the derivative via motion, slope, and functional dependence."
        ),
        "s4_editorial": (
            "Removed repetitive phrases and non-essential commentary.\n\n"
            "Replaced vague “speed” wording with precise “rate of change” / “slope coefficient”."
        ),

        "s5_title": "Geometric–algebraic analysis of exponential and logarithmic functions",
        "s5_text": (
            "This section examines exponential and logarithmic functions within a geometric–algebraic framework. "
            "The analysis relies on the algebraic tangent criterion and the concept of local linear approximation."
        ),
        "s5_select_mode": "Function type",
        "exp_mode": "Exponential ($e^x$)",
        "log_mode": "Logarithmic ($\\log_a x$)",
        "s5_exp_info": (
            "The exponential function is characterized by the property:\n\n"
            "$$\\frac{d}{dx}e^x = e^x.$$"
        ),
        "s5_log_info": (
            "For the logarithmic function:\n\n"
            "$$\\frac{d}{dx}\\log_a(x)=\\frac{1}{x\\ln(a)}.$$"
        ),
        "bases": ["e (natural)", "10 (decimal)", "2 (binary)"],
        "base_select": "Choose base",
        "calc_log": "Analyze",
        "value_eq_slope": "At the chosen point, the function value equals the slope of the tangent line.",
        "s5_conc": (
            "The derivatives are interpreted as slopes of local linear approximations, linking geometric intuition with formal analytic results."
        ),
        "s5_editorial": (
            "Removed duplication and tightened structure (exponential first, then logarithmic).\n\n"
            "Unified terminology and notation."
        ),

        "s6_title": "Connection with Newton and Cauchy",
        "s6_text": (
            "This section relates the geometric–algebraic approach to classical ideas formulated by Newton and Cauchy. "
            "The method does not conflict with classical analysis; instead, it provides an alternative didactic path to the same results.\n\n"
            "The derivative is first introduced as a limiting geometric object (tangent), obtained from the algebraic criterion and then formalized analytically."
        ),
        "x0_label": "Fixed point $x_0$",
        "dx_label": "Argument increment $\\Delta x$",
        "delta_f": "Function increment $\\Delta F$",
        "d_f": "Differential $dF$",
        "diff_val": "Remainder $\\Delta F - dF$",
        "kapanadze_limit_text": (
            "If $\\Delta F - dF$ behaves as a second-order infinitesimal, the algebraic criterion is satisfied and the slope identifies the derivative."
        ),
        "phys_header": "Physical interpretation (kinematics)",
        "phys_info": (
            "In physics, the derivative can be interpreted as instantaneous velocity; the tangent to a trajectory expresses the instantaneous direction consistent with inertial motion."
        ),
        "time": "Time $t$",
        "velocity_vec": "Instantaneous velocity vector",
        "trajectory": "Trajectory",
        "body": "Body",
        "inertia": "Inertial direction (tangent)",
        "ground": "Ground",
        "ballistic": "Ballistic motion model",
        "s6_editorial": (
            "Removed colloquial phrasing and redundant repetition.\n\n"
            "Standardized the increment/differential/remainder terminology.\n\n"
            "Reframed the physics interpretation in a classical mechanics register."
        ),

        "s7_title": "Limits of applicability (special cases)",
        "s7_text": (
            "We consider functions for which the algebraic criterion (divisibility of the remainder by the square) reveals non-existence of the derivative, "
            "thereby identifying methodological limits."
        ),
        "select_case": "Choose a case",
        "case_options": ["|x| at 0", "|x|^1.5 (reduced smoothness)", "x^2·sin(1/x) (oscillation)"],
        "case_abs_text": (
            "For $f(x)=|x|$ at $x=0$, one-sided slopes differ (left: $-1$, right: $1$), so uniqueness of the tangent fails."
        ),
        "case_1_text": (
            "For $|x|^{1.5}$, the criterion may fail due to the local remainder behavior and stability requirements."
        ),
        "case_2_text": (
            "For $x^2\\sin(1/x)$ near 0, rapid oscillation may prevent stabilization of the criterion."
        ),
        "conclusion": "Conclusion: the derivative does not exist in this case.",
        "left_tan": "Left tangent",
        "right_tan": "Right tangent",
        "s7_editorial": (
            "Added one-sided slope language for precision.\n\n"
            "Expressed the criterion strictly in second-order infinitesimal terms."
        ),
    }
}

# =========================
# Sidebar: language + title (title replaces Contents)
# =========================
st.sidebar.markdown(translations["KA"]["lang_label"])
lang_choice = st.sidebar.radio(
    "",
    [translations["KA"]["lang_ka"], translations["KA"]["lang_en"]],
    horizontal=True,
    key="lang_radio"
)
lang = "KA" if lang_choice == translations["KA"]["lang_ka"] else "EN"
txt = translations[lang]

# Title in sidebar corner (instead of Contents)
st.sidebar.markdown(f"<div class='sidebar-title'>{txt['main_title']}</div>", unsafe_allow_html=True)

# Navigation (without numbering)
st.sidebar.markdown(f"**{txt['nav_label']}**")
tab_selection = st.sidebar.radio("", txt["nav_options"], key="nav_radio")

# =========================
# NOTE: No big title in page body (per your request).
# Each page begins with the selected section title + sub-sections.
# =========================

# -----------------------------------------
# SECTION 1
# -----------------------------------------
if tab_selection == txt["nav_options"][0]:
    st.header(txt["s1_title"])

    st.subheader(txt["sub_context"])
    academic_box_md(txt["s1_text"])

    st.subheader(txt["sub_inputs"])
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"**{txt['s1_label_func']}**")
        func_input = st.text_input("", "x^2", key="geom_func")

        st.markdown(f"**{txt['s1_label_fixed']}**")
        x_a = st.number_input(r"$x_0$", value=1.0, step=0.1, format=FMT, key="num_a")

        st.markdown(f"**{txt['s1_label_increment']}**")
        h = st.slider(r"$\Delta x$", 0.01, 2.0, 1.0, 0.01, format=FMT, key="slider_h")

        st.markdown(f"**{txt['s1_label_param']}**")
        st.latex(r"B(x_0+\Delta x,\,f(x_0+\Delta x))")

    with col2:
        x = sp.symbols('x')
        try:
            f = sp.sympify(func_input)
            f_lamb = sp.lambdify(x, f, 'numpy')

            x0, xB = float(x_a), float(x_a + h)
            y0, yB = float(f_lamb(x0)), float(f_lamb(xB))

            slope_secant = (yB - y0) / (xB - x0)
            slope_tangent = float(sp.diff(f, x).subs(x, to_sympy_x0(x0)))

            x_range = np.linspace(x0 - 2, xB + 2, 500)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_range, y=f_lamb(x_range), name="f(x)", line=dict(color='#2196F3', width=3)))
            fig.add_trace(go.Scatter(x=x_range, y=y0 + slope_secant * (x_range - x0),
                                     name=txt["secant"], line=dict(color='#FFC107', dash='dash')))
            fig.add_trace(go.Scatter(x=x_range, y=y0 + slope_tangent * (x_range - x0),
                                     name=txt["tangent"], line=dict(color='#4CAF50', width=2)))
            fig.add_trace(go.Scatter(x=[x0, xB], y=[y0, yB], mode='markers+text', text=["A", "B"],
                                     marker=dict(size=12, color=['black', 'red'])))
            fig.update_layout(title=txt["viz_title"], height=520, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(str(e))

    st.subheader(txt["sub_editorial"])
    with st.expander(txt["sub_editorial"], expanded=False):
        academic_box_md(txt["s1_editorial"])

# -----------------------------------------
# SECTION 2
# -----------------------------------------
elif tab_selection == txt["nav_options"][1]:
    st.header(txt["s2_title"])

    st.subheader(txt["sub_context"])
    academic_box_md(f"**{txt['s2_thm_title']}**\n\n{txt['s2_thm_text']}")

    st.subheader(txt["sub_interpretation"])
    academic_box_md(txt["s2_interp"])

    st.subheader(txt["sub_inputs"])
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"**{txt['s2_label_func']}**")
        f_in = st.text_input("", "sin(x) * exp(0.5*x)", key="alg_func")

        st.markdown(f"**{txt['s2_label_x0']}**")
        x0_in = st.number_input(r"$x_0$", value=1.0, step=0.1, format=FMT, key="num_x0")

        calc_btn = st.button(txt["btn_analyze"], type="primary", key="btn_alg")

    if calc_btn:
        with col2:
            func_sym, k_res, tan_sym = algebraic_derivative(f_in, x0_in)
            if func_sym is not None:
                st.subheader(txt["sub_results"])
                st.markdown(f"**{txt['s2_res_slope']}**")
                st.latex(rf"k = {sp.latex(k_res)}")

                st.markdown(f"**{txt['s2_res_eq']}**")
                st.latex(rf"y = {sp.latex(tan_sym)}")

                x0v = float(x0_in)
                x_range = np.linspace(x0v - 2, x0v + 2, 700)

                x = sp.symbols('x')
                f_lamb = sp.lambdify(x, func_sym, 'numpy')
                t_lamb = sp.lambdify(x, tan_sym, 'numpy')

                y_f, y_t = f_lamb(x_range), t_lamb(x_range)

                denom = (x_range - x0v) ** 2
                with np.errstate(divide='ignore', invalid='ignore'):
                    remainder = (y_f - y_t) / denom
                remainder[np.isclose(x_range, x0v)] = np.nan

                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=(txt["vis_touch"], txt["proof_title"]),
                    vertical_spacing=0.12
                )
                fig.add_trace(go.Scatter(x=x_range, y=y_f, name="f(x)", line=dict(color='#2196F3')), row=1, col=1)
                fig.add_trace(go.Scatter(x=x_range, y=y_t, name=txt["tangent"], line=dict(color='#FF5722', dash='dash')), row=1, col=1)
                fig.add_trace(go.Scatter(x=x_range, y=remainder, name=txt["residue"], line=dict(color='#4CAF50', width=2)), row=2, col=1)
                fig.update_layout(height=760, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

                st.info(txt["s2_ok"])
            else:
                st.warning(txt["s2_fail"])
                st.error(str(tan_sym))

    st.subheader(txt["sub_editorial"])
    with st.expander(txt["sub_editorial"], expanded=False):
        academic_box_md(txt["s2_editorial"])

# -----------------------------------------
# SECTION 3
# -----------------------------------------
elif tab_selection == txt["nav_options"][2]:
    st.header(txt["s3_title"])

    st.subheader(txt["sub_context"])
    academic_box_md(txt["s3_text"])

    st.subheader(txt["sub_inputs"])
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown(f"**{txt['s3_label_surface']}**")
        f3_str = st.text_input("", "x^2 + y^2 - 0.5*x*y", key="3d_func")

        st.markdown(f"**{txt['s3_label_point']}**")
        x0 = st.number_input("x0", 0.0, step=0.1, format=FMT, key="x0_3d")
        y0 = st.number_input("y0", 0.0, step=0.1, format=FMT, key="y0_3d")

        btn_3d = st.button(txt["build_3d"], type="primary", key="btn_3d")

    if btn_3d:
        with col2:
            func_sym, kx, ky, z0 = solve_kapanadze_3d(f3_str, x0, y0)
            if func_sym is not None:
                st.subheader(txt["sub_results"])
                st.markdown(f"**{txt['s3_coeffs']}**")
                st.latex(rf"k_x = {sp.latex(kx)},\quad k_y = {sp.latex(ky)}")

                x_v = np.linspace(float(x0) - 2, float(x0) + 2, 45)
                X, Y = np.meshgrid(x_v, x_v)

                xs, ys = sp.symbols('x y')
                Z = sp.lambdify((xs, ys), func_sym, 'numpy')(X, Y)
                Z_plane = float(z0) + float(sp.N(kx)) * (X - float(x0)) + float(sp.N(ky)) * (Y - float(y0))

                fig = go.Figure()
                fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.82, name=txt["surface"]))
                fig.add_trace(go.Surface(z=Z_plane, x=X, y=Y, colorscale=[[0, 'red'], [1, 'red']],
                                         opacity=0.50, showscale=False, name=txt["tan_plane"]))
                fig.add_trace(go.Scatter3d(x=[float(x0)], y=[float(y0)], z=[float(z0)],
                                           mode='markers', marker=dict(size=5, color='black')))
                fig.update_layout(height=740, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

                academic_box_md(txt["s3_conc"])
            else:
                st.error(str(z0))

    st.subheader(txt["sub_editorial"])
    with st.expander(txt["sub_editorial"], expanded=False):
        academic_box_md(txt["s3_editorial"])

# -----------------------------------------
# SECTION 4
# -----------------------------------------
elif tab_selection == txt["nav_options"][3]:
    st.header(txt["s4_title"])

    st.subheader(txt["sub_context"])
    academic_box_md(txt["s4_text"])

    st.subheader(txt["sub_inputs"])
    trig_mode = st.radio(
        txt["trig_mode_select"],
        [txt["trig_standard"], txt["trig_inverse"]],
        horizontal=True,
        key="trig_mode"
    )

    col1, col2 = st.columns([1, 2])

    if trig_mode == txt["trig_standard"]:
        with col1:
            st.latex(r"\theta\ \text{(rad)}")
            angle = st.slider("", 0.0, float(2 * np.pi), 1.0, 0.1, format=FMT, key="angle_slider")
            st.latex(rf"\sin(\theta)\approx {np.sin(angle):.4f}")
            st.latex(rf"\cos(\theta)\approx {np.cos(angle):.4f}")

        with col2:
            t_vals = np.linspace(0, 2 * np.pi, 250)
            circle_x, circle_y = np.cos(t_vals), np.sin(t_vals)
            Px, Py = np.cos(angle), np.sin(angle)

            tan_dir = np.array([-Py, Px])
            tan_dir = tan_dir / (np.linalg.norm(tan_dir) + 1e-12)
            seg = 0.75
            tan_x = [Px - seg * tan_dir[0], Px + seg * tan_dir[0]]
            tan_y = [Py - seg * tan_dir[1], Py + seg * tan_dir[1]]

            fig = make_subplots(rows=1, cols=2, subplot_titles=(txt["unit_circle"], r"$y=\sin(x)$"))
            fig.add_trace(go.Scatter(x=circle_x, y=circle_y, line=dict(color='black')), row=1, col=1)
            fig.add_trace(go.Scatter(x=tan_x, y=tan_y, line=dict(color='red', width=3)), row=1, col=1)
            fig.add_trace(go.Scatter(x=[Px], y=[Py], mode='markers', marker=dict(color='blue', size=10)), row=1, col=1)

            fig.add_trace(go.Scatter(x=t_vals, y=np.sin(t_vals), line=dict(color='blue')), row=1, col=2)
            slope_x = np.linspace(angle - 0.7, angle + 0.7, 20)
            slope_y = np.sin(angle) + np.cos(angle) * (slope_x - angle)
            fig.add_trace(go.Scatter(x=slope_x, y=slope_y, line=dict(color='red', width=3)), row=1, col=2)
            fig.add_trace(go.Scatter(x=[angle], y=[np.sin(angle)], mode='markers', marker=dict(color='blue', size=10)), row=1, col=2)

            fig.update_layout(height=620, showlegend=False, template="plotly_white")
            fig.update_xaxes(range=[-1.6, 1.6], row=1, col=1)
            fig.update_yaxes(scaleanchor="x", scaleratio=1, range=[-1.6, 1.6], row=1, col=1)
            st.plotly_chart(fig, use_container_width=True)

    else:
        with col1:
            academic_box_md(txt["inv_info"])
            st.latex(r"x\in[-1,1]")
            val = st.slider("", -1.0, 1.0, 0.5, 0.01, format=FMT, key="inv_val")
            val_tan = val * 5.0

            angle_asin = float(np.arcsin(val))
            angle_acos = float(np.arccos(val))
            angle_atan = float(np.arctan(val_tan))

            st.markdown(f"**{txt['inv_res']}**")
            st.latex(rf"\arcsin({val}) = {angle_asin:.4f}\ \text{{rad}} \approx {np.degrees(angle_asin):.2f}^\circ")
            st.latex(rf"\arccos({val}) = {angle_acos:.4f}\ \text{{rad}} \approx {np.degrees(angle_acos):.2f}^\circ")
            st.latex(rf"\arctan({val_tan:.2f}) = {angle_atan:.4f}\ \text{{rad}} \approx {np.degrees(angle_atan):.2f}^\circ")

            academic_box_md(txt["s4_conc"])

        with col2:
            x_domain = np.linspace(-1, 1, 220)
            x_tan_domain = np.linspace(-5, 5, 220)

            fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=(r"$y=\arcsin(x)$", r"$y=\arccos(x)$", r"$y=\arctan(x)$"),
                vertical_spacing=0.12
            )

            fig.add_trace(go.Scatter(x=x_domain, y=np.arcsin(x_domain)), row=1, col=1)
            fig.add_trace(go.Scatter(x=[val], y=[angle_asin], mode='markers', marker=dict(size=10, color='red')), row=1, col=1)

            fig.add_trace(go.Scatter(x=x_domain, y=np.arccos(x_domain)), row=2, col=1)
            fig.add_trace(go.Scatter(x=[val], y=[angle_acos], mode='markers', marker=dict(size=10, color='red')), row=2, col=1)

            fig.add_trace(go.Scatter(x=x_tan_domain, y=np.arctan(x_tan_domain)), row=3, col=1)
            fig.add_trace(go.Scatter(x=[val_tan], y=[angle_atan], mode='markers', marker=dict(size=10, color='red')), row=3, col=1)

            fig.update_layout(height=820, showlegend=False, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader(txt["sub_editorial"])
    with st.expander(txt["sub_editorial"], expanded=False):
        academic_box_md(txt["s4_editorial"])

# -----------------------------------------
# SECTION 5 (LOG FIXED)
# -----------------------------------------
elif tab_selection == txt["nav_options"][4]:
    st.header(txt["s5_title"])

    st.subheader(txt["sub_context"])
    academic_box_md(txt["s5_text"])

    st.subheader(txt["sub_inputs"])
    col1, col2 = st.columns([1, 2])

    with col1:
        func_mode = st.radio(
            txt["s5_select_mode"],
            [txt["exp_mode"], txt["log_mode"]],
            horizontal=True,
            key="func_mode_5"
        )

        if func_mode == txt["exp_mode"]:
            academic_box_md(txt["s5_exp_info"])

            x0_exp = st.number_input(r"$x_0$", value=1.0, step=0.1, format=FMT, key="x0_exp")
            val = float(np.exp(x0_exp))
            slope = val

            st.subheader(txt["sub_results"])
            st.latex(rf"f(x_0)=e^{{{x0_exp}}}\approx {val:.6f}")
            st.latex(rf"f'(x_0)=e^{{{x0_exp}}}\approx {slope:.6f}")
            st.caption(txt["value_eq_slope"])

            x_range = np.linspace(float(x0_exp) - 2, float(x0_exp) + 2, 220)
            y_exp = np.exp(x_range)
            y_tan = val + slope * (x_range - float(x0_exp))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_range, y=y_exp, name=r"$e^x$"))
            fig.add_trace(go.Scatter(x=x_range, y=y_tan, name=txt["tangent"], line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=[float(x0_exp)], y=[val], mode='markers+text', text=["P"], textposition="top left"))
            fig.update_layout(title=r"$y=e^x$", height=520, template="plotly_white")

            with col2:
                st.plotly_chart(fig, use_container_width=True, key="chart_exp")

            academic_box_md(txt["s5_conc"])

        else:
            academic_box_md(txt["s5_log_info"])

            base_type = st.selectbox(txt["base_select"], txt["bases"], key="base_select_5")
            x0_log = st.number_input(r"$x_0\ (>0)$", value=1.0, step=0.1, min_value=0.01, format=FMT, key="x0_log")

            x = sp.symbols('x')

            # IMPORTANT: use expressions that lambdify reliably
            if base_type.startswith("e"):
                func_sym = sp.log(x)                # ln(x)
                a_display = "e"
                display_str = r"$\ln(x)$"
            elif base_type.startswith("10"):
                func_sym = sp.log(x) / sp.log(10)   # log10(x)
                a_display = "10"
                display_str = r"$\log_{10}(x)$"
            else:
                func_sym = sp.log(x) / sp.log(2)    # log2(x)
                a_display = "2"
                display_str = r"$\log_{2}(x)$"

            if st.button(txt["calc_log"], type="primary", key="btn_log_5"):
                func_used, k_res, tan_sym = algebraic_derivative(func_sym, x0_log)
                if func_used is not None:
                    st.subheader(txt["sub_results"])
                    st.latex(rf"f'(x_0)=\frac{{1}}{{x_0\ln({a_display})}} = {sp.latex(k_res)}")
                    st.latex(rf"y = {sp.latex(tan_sym)}")

                    x0v = float(x0_log)
                    x_start = max(0.01, x0v - 2.0)
                    x_range = np.linspace(x_start, x0v + 2.0, 520)

                    f_lamb = sp.lambdify(x, func_used, 'numpy')
                    t_lamb = sp.lambdify(x, tan_sym, 'numpy')
                    y_f, y_t = f_lamb(x_range), t_lamb(x_range)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x_range, y=y_f, name=display_str))
                    fig.add_trace(go.Scatter(x=x_range, y=y_t, name=txt["tangent"], line=dict(dash='dash')))
                    fig.add_trace(go.Scatter(x=[x0v], y=[float(f_lamb(x0v))], mode='markers'))
                    fig.update_layout(title=f"Graph: {display_str}", height=520, template="plotly_white")

                    with col2:
                        st.plotly_chart(fig, use_container_width=True, key="chart_log")

                    academic_box_md(txt["s5_conc"])
                else:
                    st.warning(txt["s2_fail"])
                    st.error(str(tan_sym))

    st.subheader(txt["sub_editorial"])
    with st.expander(txt["sub_editorial"], expanded=False):
        academic_box_md(txt["s5_editorial"])

# -----------------------------------------
# SECTION 6
# -----------------------------------------
elif tab_selection == txt["nav_options"][5]:
    st.header(txt["s6_title"])

    st.subheader(txt["sub_context"])
    academic_box_md(txt["s6_text"])

    st.subheader(txt["sub_inputs"])
    col1, col2 = st.columns([1, 2])

    with col1:
        x0 = st.number_input(txt["x0_label"], value=1.0, step=0.1, format=FMT, key="nc_x0")
        dx = st.slider(txt["dx_label"], 0.01, 2.0, 1.0, 0.01, format=FMT, key="nc_dx")

        x = sp.symbols('x')
        f = sp.sympify("x^2")
        f_lamb = sp.lambdify(x, f, 'numpy')

        y0 = float(f_lamb(float(x0)))
        y_next = float(f_lamb(float(x0 + dx)))

        delta_F = y_next - y0
        k = float(sp.diff(f, x).subs(x, to_sympy_x0(x0)))
        dF = k * float(dx)
        rem = delta_F - dF

        st.subheader(txt["sub_results"])
        st.markdown(f"**{txt['delta_f']}**")
        st.latex(rf"{delta_F:.6f}")

        st.markdown(f"**{txt['d_f']}**")
        st.latex(rf"{dF:.6f}")

        st.markdown(f"**{txt['diff_val']}**")
        st.latex(rf"{rem:.6f}")

        st.info(txt["kapanadze_limit_text"])

    with col2:
        x_range = np.linspace(float(x0) - 0.8, float(x0 + dx) + 0.8, 260)
        y_curve = f_lamb(x_range)
        y_tan = y0 + k * (x_range - float(x0))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_range, y=y_curve, name="F(x)"))
        fig.add_trace(go.Scatter(x=x_range, y=y_tan, name="Tangent", line=dict(dash='dash')))
        fig.update_layout(title="Newton–Cauchy geometric correspondence (demonstration)", height=620,
                          showlegend=False, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader(txt["phys_header"])
    academic_box_md(txt["phys_info"])

    col1, col2 = st.columns([1, 2])

    with col1:
        t = st.slider(txt["time"], 0.0, 2.0, 0.5, 0.05, format=FMT, key="phys_time")
        x_val = t
        y_val = -(t ** 2) + 2
        vy = -2 * t
        st.markdown(f"**{txt['velocity_vec']}**")
        st.latex(rf"(1,\ {vy:.4f})")

    with col2:
        t_range = np.linspace(0, 2, 220)
        x_traj = t_range
        y_traj = -(t_range ** 2) + 2

        slope = vy
        x_tan = np.linspace(x_val, x_val + 0.6, 12)
        y_tan = y_val + slope * (x_tan - x_val)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_traj, y=y_traj, name=txt["trajectory"]))
        fig.add_trace(go.Scatter(x=[x_val], y=[y_val], mode='markers', marker=dict(size=12), name=txt["body"]))
        fig.add_trace(go.Scatter(x=x_tan, y=y_tan, name=txt["inertia"], line=dict(width=3)))
        fig.add_trace(go.Scatter(x=[0, 2], y=[-2, -2], name=txt["ground"], line=dict(width=5)))
        fig.update_layout(title=txt["ballistic"], height=520,
                          yaxis=dict(range=[-2.5, 2.5], scaleanchor="x", scaleratio=1),
                          template="plotly_white")
        st.plotly_chart(fig, use_container_width=True, key="phys_chart")

    st.subheader(txt["sub_editorial"])
    with st.expander(txt["sub_editorial"], expanded=False):
        academic_box_md(txt["s6_editorial"])

# -----------------------------------------
# SECTION 7
# -----------------------------------------
elif tab_selection == txt["nav_options"][6]:
    st.header(txt["s7_title"])

    st.subheader(txt["sub_context"])
    academic_box_md(txt["s7_text"])

    st.subheader(txt["sub_inputs"])
    col1, col2 = st.columns([1, 2])

    with col1:
        problem_label = st.selectbox(txt["select_case"], txt["case_options"], key="case_select")

        st.subheader(txt["sub_interpretation"])
        if "|x|" in problem_label and "1.5" not in problem_label:
            academic_box_md(txt["case_abs_text"])
            problem_type = "abs"
        elif "1.5" in problem_label:
            academic_box_md(txt["case_1_text"])
            problem_type = "1.5"
        else:
            academic_box_md(txt["case_2_text"])
            problem_type = "osc"

    with col2:
        x = np.linspace(-1, 1, 1200)

        if problem_type == "abs":
            y = np.abs(x)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, name="|x|"))
            fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], name=f"{txt['right_tan']} (k=1)", line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=[-1, 0], y=[1, 0], name=f"{txt['left_tan']} (k=-1)", line=dict(dash='dash')))
            fig.update_layout(title=r"$y=|x|$ at $x=0$ (non-unique tangent)", height=520, template="plotly_white")

        elif problem_type == "1.5":
            x_pos, x_neg = np.linspace(0, 1, 600), np.linspace(-1, 0, 600)
            y_pos, y_neg = x_pos ** 1.5, np.abs(x_neg) ** 1.5
            x_all = np.concatenate([x_neg, x_pos])
            y_all = np.concatenate([y_neg, y_pos])

            tangent = np.zeros_like(x_all)
            with np.errstate(divide='ignore', invalid='ignore'):
                remainder = y_all / (x_all ** 2)
            remainder[np.isclose(x_all, 0.0)] = np.nan

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_all, y=y_all, name=r"$|x|^{1.5}$"))
            fig.add_trace(go.Scatter(x=x_all, y=tangent, name=txt["tangent"], line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=x_all, y=remainder, name=txt["residue"]))
            fig.update_layout(title="Local remainder behavior (illustration)", height=620,
                              yaxis=dict(range=[0, 6]), template="plotly_white")

        else:
            eps = 1e-9
            y = (x ** 2) * np.sin(1 / (x + eps))
            with np.errstate(divide='ignore', invalid='ignore'):
                remainder = np.sin(1 / (x + eps))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, name="f(x)"))
            fig.add_trace(go.Scatter(x=x, y=remainder, name=txt["residue"]))
            fig.update_layout(title="Oscillation and stabilization failure (illustration)", height=620,
                              yaxis=dict(range=[-2, 2]), template="plotly_white")

        st.plotly_chart(fig, use_container_width=True)
        st.info(txt["conclusion"])

    st.subheader(txt["sub_editorial"])
    with st.expander(txt["sub_editorial"], expanded=False):
        academic_box_md(txt["s7_editorial"])
