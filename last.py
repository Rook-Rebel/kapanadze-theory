import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

# --- გვერდის კონფიგურაცია ---
st.set_page_config(
    page_title="Derivative Analysis Model",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS დიზაინი (აკადემიური სტილი) ---
st.markdown("""
<style>
    /* Journal-style layout */
    .main .block-container {
        max-width: 1100px;
        margin: 0 auto;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 1.8rem;
        padding-right: 1.8rem;
    }
    
    .stApp {
        background-color: #ffffff;
        color: #1f2937;
    }

    p, li, label, div, span {
        font-family: 'Georgia', serif;
        line-height: 1.78;
    }

    h1 { 
        font-size: 2.05rem !important; 
        font-weight: 650 !important; 
        font-family: 'Times New Roman', Times, serif; 
        color: #1f2937;
        letter-spacing: 0.1px;
    }
    h2, h3, h4 { 
        font-family: 'Times New Roman', Times, serif; 
        color: #202a36;
        font-weight: 600 !important;
    }
    
    /* Academic box via markdown blockquote (LaTeX-safe) */
    blockquote {
        margin: 0.85rem 0 1.15rem 0 !important;
        padding: 0.95rem 1.1rem !important;
        border-radius: 12px !important;
        background: #fbfbfc !important;
        border: 1px solid #e7e8ec !important;
        border-left: 4px solid #2f3a46 !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
        font-family: 'Georgia', serif;
        color: #1f2937;
        line-height: 1.8;
    }
    blockquote p {
        margin: 0.2rem 0 !important;
    }
    
    hr {
        border: none;
        border-top: 1px solid #e8eaef;
        margin-top: 1.2rem;
        margin-bottom: 1.25rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #f7f8fa;
        border-right: 1px solid #e3e6eb;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Georgia', serif;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-family: 'Times New Roman', Times, serif !important;
        color: #1f2937 !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1f2a36;
        color: white;
        border-radius: 8px;
        border: 1px solid #1f2a36;
        font-family: 'Times New Roman', Times, serif;
        padding: 0.45rem 0.95rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #18212b;
        border-color: #18212b;
        box-shadow: 0 2px 6px rgba(17, 24, 39, 0.15);
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --- თარგმანების ლექსიკონი ---
translations = {
    "KA": {
        "sidebar_title": "სტრუქტურა (კვლევები)",
        "nav_options": [
            "I. შემხები წრფის გეომეტრიული წარმოშობა",
            "II. ალგებრული კრიტერიუმი",
            "III. სივრცითი განზოგადება",
            "IV. ტრიგონომეტრიული ფუნქციები",
            "V. მაჩვენებლიანი და ლოგარითმული ფუნქციები",
            "VI. კავშირი კლასიკურ ანალიზთან",
            "VII. მეთოდის გამოყენების საზღვრები"
        ],
        "title": "ინტერაქტიული მოდელი წარმოებულის გეომეტრიული და ალგებრული ინტერპრეტაციისათვის",
        "bases": ["e (ნატურალური ln)", "10 (ათობითი)", "2 (ორობითი)"],
        
        # Tab 1
        "t1_header": "მკვეთი წრფის თანმიმდევრული მიახლოება შემხებ წრფასთან",
        "t1_info": "შემხები წრფა განიხილება, როგორც მკვეთი წრფის ზღვრული შემთხვევა, როდესაც მოძრავი წერტილი თანმიმდევრულად უახლოვდება ფუნქციის გრაფიკზე ფიქსირებულ წერტილს.",
        "func_label": "ფუნქცია",
        "point_a": "ფიქსირებული წერტილი (A)",
        "point_b_dist": "მეორე წერტილის დაშორება (h)",
        "secant": "მკვეთი წრფე",
        "tangent": "შემხები წრფე",
        "viz_title": "გეომეტრიული ვიზუალიზაცია",
        
        # Tab 2
        "t2_header": "ნაშთის კვადრატზე გაყოფის ალგებრული მეთოდი",
        "t2_thm_title": "ალგებრული კრიტერიუმი შემხები წრფისათვის",
        "t2_thm_text": "წრფე წარმოადგენს ფუნქციის შემხებ წრფეს მოცემულ წერტილში მაშინ და მხოლოდ მაშინ, როდესაც ფუნქციისა და წრფის სხვაობა იყოფა ნაშთის კვადრატზე.",
        "t2_thm_sub": "ეს პირობა ნიშნავს, რომ ფუნქციისა და მისი შემხები წრფის სხვაობა $x_0$-ის მახლობლად არის მეორე რიგის უსასრულოდ მცირე სიდიდე. შესაბამისად, ნაშთის გრაფიკი არ ავლენს უსასრულოდ ზრდად ქცევას შეხების წერტილის მახლობლად.",
        "touch_point": "შეხების წერტილი",
        "calc_btn": "გამოთვლა და ანალიზი",
        "result": "შედეგი",
        "slope_found": "დახრილობის კოეფიციენტი (k)",
        "tan_eq": "შემხები წრფის განტოლება",
        "proof_title": "ნაშთის ანალიზი",
        "vis_touch": "ფუნქცია და შემხები",
        "residue": "ნაშთი",
        "success_msg": "✔ კრიტერიუმის შესრულება: ნაშთი აკმაყოფილებს ალგებრულ კრიტერიუმს და წარმოადგენს მეორე რიგის უსასრულოდ მცირე სიდიდეს, რის შედეგადაც შემხები წრფის არსებობა დადასტურებულია.",
        "error_msg": "შეცდომა",
        
        # Tab 3
        "t3_header": "კაპანაძის მიდგომის სივრცითი განზოგადება",
        "t3_intro": "ერთგანზომილებიანი შემთხვევის ანალოგიურად, სამგანზომილებიან სივრცეში განიხილება ზედაპირი:",
        "t3_info": "შემხები სიბრტყე განისაზღვრება იმ პირობით, რომ ფუნქციისა და შესაბამისი სიბრტყის სხვაობა აღნიშნული წერტილის მახლობლად წარმოადგენს მეორე რიგის უსასრულოდ მცირე სიდიდეს. ეს ალგებრული კრიტერიუმი უზრუნველყოფს შემხები სიბრტყის არსებობასა და უნიკალურობას და იძლევა დიფერენციალური გეომეტრიის ბუნებრივ ინტერპრეტაციას, ზღვრის ცნების უშუალო გამოყენების გარეშე საწყის ეტაპზე.",
        "surface_label": "ზედაპირი",
        "build_3d": "3D მოდელის აგება",
        "found_partials": "დახრილობის კოეფიციენტები",
        "surface": "ზედაპირი",
        "tan_plane": "შემხები სიბრტყე",
        "t3_res_text": "ეს ნიშნავს, რომ მოცემულ წერტილში შემხები სიბრტყე პარალელურია $xy$-სიბრტყის და წარმოადგენს ზედაპირის ლოკალურ ლინეურ მიახლოებას.",
        
        # Tab 4
        "t4_header": "ტრიგონომეტრიული ფუნქციების გეომეტრიულ–ალგებრული ანალიზი",
        "t4_intro_long": """
        წარმოდგენილი მოდელი ეფუძნება ტრიგონომეტრიული ფუნქციების წარმოებულების გეომეტრიულ და ალგებრულ ინტერპრეტაციას. ანალიზი ხორციელდება ერთეულოვან წრეწირზე წერტილის მოძრაობის მოდელის გამოყენებით, რაც უზრუნველყოფს კუთხესა და შესაბამის ფუნქციურ მნიშვნელობებს შორის დამოკიდებულების გეომეტრიულ გააზრებას.
        
        ერთეულოვან წრეწირზე მოძრაობისას სინუსისა და კოსინუსის ფუნქციები განიხილება, როგორც კოორდინატული პროექციები, ხოლო კოსინუსის მნიშვნელობა ინტერპრეტირდება, როგორც სინუსის ფუნქციის შესაბამისი შემხები წრფის დახრილობის კოეფიციენტი.
        
        ამგვარად, ტრიგონომეტრიული ფუნქციების გეომეტრიულ–ალგებრული წარმოდგენა ბუნებრივად აკავშირებს ერთეულოვან წრეწირს, ფუნქციის ცვლილების სიჩქარესა და წარმოებულის ცნებას.
        """,
        "angle": "კუთხე",
        "slope": "დახრილობა",
        "unit_circle": "ერთეულოვანი წრეწირი",
        "trig_mode_select": "ვიზუალიზაციის რეჟიმი",
        "trig_standard": "ტრიგონომეტრიული წრეწირი",
        "trig_inverse": "შებრუნებული ფუნქციები",
        "input_val": "არგუმენტის მნიშვნელობა",
        "inv_res": "შედეგები",
        "inv_info": "შებრუნებული ტრიგონომეტრიული ფუნქციების ეს გეომეტრიულ–ალგებრული წარმოდგენა უზრუნველყოფს წარმოებულის ცნების კონცეპტუალურ გააზრებას მოძრაობის, დახრილობისა და ფუნქციური დამოკიდებულების საფუძველზე.",
        "t4_conc": "კონცეპტუალური დასკვნა",
        "t4_conc_text": "ტრიგონომეტრიული და შებრუნებული ტრიგონომეტრიული ფუნქციების წარმოდგენილი მოდელი უზრუნველყოფს წარმოებულის ცნების კონცეპტუალურ გააზრებას მოძრაობის, დახრილობისა და ფუნქციური დამოკიდებულების საფუძველზე. აღნიშნული მიდგომა ქმნის ბუნებრივ გარდამავალ საფეხურს კლასიკური მათემატიკური ანალიზის ფორმალურ განსაზღვრებამდე.",
        
        # Tab 5
        "t5_header": "მაჩვენებლიანი და ლოგარითმული ფუნქციების გეომეტრიულ–ალგებრული ანალიზი",
        "t5_intro": "მოცემულ თავში განიხილება მაჩვენებლიანი და ლოგარითმული ფუნქციები კაპანაძის გეომეტრიულ–ალგებრული მიდგომის ფარგლებში. ანალიზი ეფუძნება შემხები წრფის ალგებრულ კრიტერიუმს და ფუნქციის ლოკალური ლინეური მიახლოების იდეას.",
        "t5_select_mode": "ფუნქციის ტიპი",
        "t5_exp_desc": "მაჩვენებლიანი ფუნქცია $e^x$ ხასიათდება იმ თვისებით, რომ მისი წარმოებული ყველა წერტილში ემთხვევა თავად ფუნქციის მნიშვნელობისა:",
        "t5_log_desc": "კაპანაძის მეთოდის ფარგლებში ლოგარითმული ფუნქციის წარმოებული მიიღება ალგებრული კრიტერიუმის გამოყენებით:",
        "value_eq_slope": "ამგვარად, მოცემულ წერტილში ფუნქციის მნიშვნელობა და შესაბამისი შემხები წრფის დახრილობის კოეფიციენტი ერთმანეთს ემთხვევა, რაც წარმოადგენს $e^x$-ის ფუნდამენტურ გეომეტრიულ თვისებას.",
        "base_select": "ფუძის არჩევა",
        "calc_log": "ანალიზი",
        "residue_analysis": "ნაშთის ქცევა",
        "graph": "გრაფიკი",
        "t5_conc": "კონცეპტუალური დასკვნა",
        "t5_conc_text": "მაჩვენებლიანი და ლოგარითმული ფუნქციების წარმოდგენილი გეომეტრიულ–ალგებრული ანალიზი აჩვენებს, რომ მათი წარმოებულები განისაზღვრება შემხები წრფის ალგებრული კრიტერიუმის საფუძველზე და ინტერპრეტირდება როგორც ლოკალური ლინეური მიახლოების დახრილობა. აღნიშნული მიდგომა ქმნის ბუნებრივ კავშირს გეომეტრიულ ინტუიციასა და კლასიკური ანალიზის ფორმალურ შედეგებს შორის.",
        
        # Tab 6
        "t6_header": "კავშირი კლასიკურ ანალიზთან (ნიუტონი და კოში)",
        "t6_intro": "კაპანაძის მიდგომაში წარმოებული თავდაპირველად განიხილება, როგორც ზღვრული გეომეტრიული ობიექტი — ფუნქციის გრაფიკზე აგებული შემხები წრფე, რომელიც მიიღება ალგებრული კრიტერიუმის შესრულების შედეგად და შემდგომ იღებს ზღვრულ ანალიტიკურ ინტერპრეტაციას.",
        "t6_sec_incr": "ფუნქციის ნაზრდი და დიფერენციალი",
        "t6_fixed": "ფიქსირებული წერტილი:",
        "t6_arg_incr": "არგუმენტის ნაზრდი:",
        "t6_func_incr": "ფუნქციის ნაზრდი:",
        "t6_geom_bc": "რომელიც გეომეტრიულად შეესაბამება მონაკვეთს $BC$.",
        "t6_diff": "დიფერენციალი:",
        "t6_geom_bn": "რომელიც გეომეტრიულად შეესაბამება მონაკვეთს $BN$.",
        "t6_rem": "ნაშთი (სხვაობა):",
        "t6_geom_nc": "რაც წარმოდგენილია მონაკვეთის $NC$ სახით.",
        "t6_sec_alg": "ალგებრული კრიტერიუმი",
        "t6_alg_text": "თუ სხვაობა $\Delta F - dF$ არგუმენტის ნაზრდის შემცირებისას მცირდება ისე, რომ წარმოადგენს მეორე რიგის უსასრულოდ მცირე სიდიდეს, მაშინ შესრულებულია კაპანაძის ალგებრული კრიტერიუმი. ამგვარად, ზღვრული პროცესი არ გამოიყენება საწყის განსაზღვრებად, არამედ ჩნდება, როგორც უკვე აგებული გეომეტრიულ–ალგებრული კონსტრუქციის ანალიტიკური ფორმალიზაცია.",
        
        "t8_header": "ფიზიკური ინტერპრეტაცია (კინემატიკა)",
        "t8_info": "ფიზიკურ კონტექსტში წარმოებული განიხილება, როგორც მოძრაობის მომენტალური მახასიათებელი. კერძოდ, ტრაექტორიაზე აგებული შემხები წრფე აღწერს სხეულის იმ მომენტალურ მიმართულებას, რომელსაც იგი გაყვებოდა მოცემულ მომენტში, თუ მასზე მოქმედი გარე ძალები შეწყდებოდა (ინერციული მოძრაობის პრინციპი).",
        "time": "დრო",
        "velocity_vec": "მომენტალური სიჩქარის ვექტორი",
        "trajectory": "ტრაექტორია",
        "body": "სხეული",
        "inertia": "ინერცია (შემხები)",
        "ground": "ზედაპირი",
        "ballistic": "ბალისტიკური მოძრაობის სიმულაცია",
        "t6_conc": "კონცეპტუალური დასკვნა",
        "t6_conc_text": "კაპანაძის ალგებრული–გეომეტრიული მიდგომა ქმნის ბუნებრივ კონცეპტუალურ ხიდს კოშის ზღვრულ ფორმალიზმს შორის. წარმოებული აქ არ განისაზღვრება უშუალოდ ლიმიტის ფორმულით; იგი მიიღება გეომეტრიულად და ალგებრულად დასაბუთებული კონსტრუქციის შედეგად, ხოლო ზღვრული ინტერპრეტაცია წარმოადგენს ამ კონსტრუქციის ანალიტიკურ ფორმალიზაციას.",

        # Tab 7
        "t7_header": "მეთოდის გამოყენების საზღვრები (განსაკუთრებული შემთხვევები)",
        "t7_info": "კაპანაძის ალგებრული–გეომეტრიული მიდგომა.",
        "t7_intro_main": "წარმოდგენილ ქვეთავში განიხილება ისეთი ფუნქციები, რომელთა შემთხვევაში ნაშთის კვადრატზე გაყოფის ალგებრული კრიტერიუმი იძლევა სპეციფიკურ შედეგს და ნათლად ავლენს მეთოდის გამოყენების საზღვრებს.",
        "select_case": "აირჩიეთ შემთხვევა",
        "case_options": ["|x| (მოდული 0-ში)", "|x|^1.5 (ნაკლები სიგლუვე)", "x^2 * sin(1/x) (ოსცილაცია)"],
        "case_abs_title": "მოდულის ფუნქცია წერტილში $x=0$",
        "case_abs_text": "წერტილში $x=0$ ფუნქციის გრაფიკს გააჩნია ორი განსხვავებული შემხები წრფე: მარცხენა მხრიდან დახრილობის კოეფიციენტი ტოლია $-1$, ხოლო მარჯვენა მხრიდან $1$. ამგვარად, მოცემულ წერტილში შემხები წრფის უნიკალურობა ირღვევა, რაც წარმოებულის არსებობის აუცილებელ პირობას არ აკმაყოფილებს.",
        "t7_alg_interp_title": "ალგებრული ინტერპრეტაცია",
        "t7_alg_interp_text": "კაპანაძის ალგებრული კრიტერიუმის მიხედვით, წარმოებულის არსებობა დაკავშირებულია იმ პირობასთან, რომ ფუნქციისა და შესაბამისი ლინეური მიახლოების სხვაობა იყოს მეორე რიგის უსასრულოდ მცირე სიდიდე. ფუნქციის $f(x)=|x|$ შემთხვევაში აღნიშნული პირობა წერტილში $x=0$ არ სრულდება, რადგან ნაშთის ქცევა მარცხენა და მარჯვენა მხრიდან განსხვავებულია.",
        "t7_conc_title": "დასკვნა",
        "t7_conc_text": "მოცემულ განსაკუთრებულ შემთხვევაში კაპანაძის ალგებრული კრიტერიუმი ცალსახად მიუთითებს, რომ წარმოებული არ არსებობს. აღნიშნული მაგალითი ადასტურებს, რომ მეთოდი არა მხოლოდ წარმოებულის არსებობის დასადგენად, არამედ მისი არარსებობის დიაგნოსტიკისათვისაც ეფექტიანად გამოიყენება.",
        "case_1_text": "ფუნქციას აქვს წარმოებული, მაგრამ ნაშთი არ მცირდება საკმარისად სწრაფად.",
        "case_2_text": "ფუნქცია ირხევა ძალიან სწრაფად, რის გამოც ნაშთი არ სტაბილურდება.",
        "left_tan": "მარცხენა მხები",
        "right_tan": "მარჯვენა მხები"
    },
    "EN": {
        "sidebar_title": "Structure (Research)",
        "nav_options": [
            "I. Geometric Origin of the Tangent Line",
            "II. Algebraic Criterion",
            "III. Spatial Generalization",
            "IV. Trigonometric Functions",
            "V. Exponential and Logarithmic Functions",
            "VI. Connection with Classical Analysis",
            "VII. Limits of Method Applicability"
        ],
        "title": "Interactive Model for Geometric and Algebraic Interpretation of the Derivative",
        "bases": ["e (Natural ln)", "10 (Decimal)", "2 (Binary)"],
        
        # Tab 1
        "t1_header": "Successive Approximation of the Secant Line to the Tangent Line",
        "t1_info": "The tangent line is considered as the limiting case of the secant line, when the moving point successively approaches a fixed point on the graph of the function.",
        "func_label": "Function",
        "point_a": "Fixed point (A)",
        "point_b_dist": "Distance to second point (h)",
        "secant": "Secant",
        "tangent": "Tangent",
        "viz_title": "Visualization",
        
        # Tab 2
        "t2_header": "Algebraic Method",
        "t2_thm_title": "Algebraic Criterion for the Tangent Line",
        "t2_thm_text": "A line is a tangent to the function at a given point if and only if the difference between the function and the line is divisible by the square of the increment.",
        "t2_thm_sub": "This condition means that the difference between the function and its tangent line near $x_0$ is an infinitesimal quantity of second order. Consequently, the remainder graph does not exhibit infinitely increasing behavior near the touching point.",
        "touch_point": "Point of tangency",
        "calc_btn": "Compute and Analyze",
        "result": "Result",
        "slope_found": "Slope coefficient (k)",
        "tan_eq": "Tangent line equation",
        "proof_title": "Remainder Analysis",
        "vis_touch": "Function and Tangent",
        "residue": "Residue",
        "success_msg": "✔ Criterion satisfied: the residue meets the algebraic criterion and is an infinitesimal quantity of second order, confirming the existence of the tangent line.",
        "error_msg": "Error",
        
        # Tab 3
        "t3_header": "Spatial Generalization",
        "t3_intro": "Analogous to the one-dimensional case, in three-dimensional space we consider the surface:",
        "t3_info": "The tangent plane is determined by the condition that the difference between the function and the corresponding plane near the given point is an infinitesimal quantity of second order. This algebraic criterion ensures the existence and uniqueness of the tangent plane and provides a natural interpretation of differential geometry, without direct use of the limit concept at the initial stage.",
        "surface_label": "Surface",
        "build_3d": "Build 3D Model",
        "found_partials": "Slope coefficients",
        "surface": "Surface",
        "tan_plane": "Tangent Plane",
        "t3_res_text": "This means that, at the given point, the tangent plane is parallel to the $xy$-plane and represents the local linear approximation of the surface.",
        
        # Tab 4
        "t4_header": "Trigonometric Analysis",
        "t4_intro_long": """
        The presented model is based on geometric and algebraic interpretations of derivatives of trigonometric functions. The analysis is carried out using a model of point motion on the unit circle, which provides a geometric understanding of the relationship between the angle and corresponding function values.
        
        During motion on the unit circle, sine and cosine functions are considered as coordinate projections, while the cosine value is interpreted as the slope coefficient of the tangent line to the sine function.
        
        Thus, the geometric–algebraic representation of trigonometric functions naturally connects the unit circle, the rate of function change, and the concept of derivative.
        """,
        "angle": "Angle",
        "slope": "Slope",
        "unit_circle": "Unit Circle",
        "trig_mode_select": "Visualization Mode",
        "trig_standard": "Trigonometric Circle",
        "trig_inverse": "Inverse Functions",
        "input_val": "Input value",
        "inv_res": "Results",
        "inv_info": "This geometric–algebraic representation of inverse trigonometric functions provides a conceptual understanding of the derivative based on motion, slope, and functional dependence.",
        "t4_conc": "Conclusion",
        "t4_conc_text": "The presented model of trigonometric and inverse trigonometric functions provides a conceptual understanding of the derivative based on motion, slope, and functional dependence. This approach creates a natural transitional step to formal definitions in classical mathematical analysis.",
        
        # Tab 5
        "t5_header": "Geometric–Algebraic Analysis of Exponential and Logarithmic Functions",
        "t5_intro": "In this chapter, exponential and logarithmic functions are considered within Kapanadze’s geometric–algebraic approach. The analysis is based on the algebraic criterion of the tangent line and the idea of local linear approximation.",
        "t5_select_mode": "Function Type",
        "t5_exp_desc": "The exponential function $e^x$ is characterized by the property that its derivative at every point equals the value of the function itself:",
        "t5_log_desc": "Within Kapanadze’s method, the derivative of the logarithmic function is obtained using the algebraic criterion:",
        "value_eq_slope": "Thus, at the given point, the function value and the corresponding tangent line slope coefficient coincide, which is a fundamental geometric property of $e^x$.",
        "base_select": "Base",
        "calc_log": "Analyze",
        "residue_analysis": "Remainder behavior",
        "graph": "Graph",
        "t5_conc": "Conclusion",
        "t5_conc_text": "The presented geometric–algebraic analysis of exponential and logarithmic functions shows that their derivatives are determined by the algebraic criterion of the tangent line and interpreted as the slope of local linear approximation. This approach creates a natural connection between geometric intuition and formal results of classical analysis.",
        
        # Tab 6
        "t6_header": "Connection with Classical Analysis",
        "t6_intro": "In Kapanadze’s approach, the derivative is initially considered as a limiting geometric object — a tangent line constructed on the graph of a function, obtained through fulfillment of an algebraic criterion and later given a limit-based analytical interpretation.",
        "t6_sec_incr": "Function Increment and Differential",
        "t6_fixed": "Fixed point:",
        "t6_arg_incr": "Argument increment:",
        "t6_func_incr": "Function increment:",
        "t6_geom_bc": "which geometrically corresponds to segment $BC$.",
        "t6_diff": "Differential:",
        "t6_geom_bn": "which geometrically corresponds to segment $BN$.",
        "t6_rem": "Remainder (difference):",
        "t6_geom_nc": "which is represented by segment $NC$.",
        "t6_sec_alg": "Algebraic Criterion",
        "t6_alg_text": "If the difference $\Delta F - dF$ decreases as the argument increment shrinks so that it represents an infinitesimal quantity of second order, then Kapanadze’s algebraic criterion is satisfied. Thus, the limit process is not used as the initial definition, but appears as an analytical formalization of an already constructed geometric–algebraic structure.",
        "t8_header": "Physical Interp",
        "t8_info": "In a physical context, the derivative is viewed as an instantaneous characteristic of motion. In particular, the tangent line constructed on the trajectory describes the instantaneous direction the body would follow at that moment if external forces ceased (principle of inertial motion).",
        "time": "Time",
        "velocity_vec": "Instantaneous velocity vector",
        "trajectory": "Trajectory",
        "body": "Body",
        "inertia": "Inertia",
        "ground": "Ground",
        "ballistic": "Ballistic",
        "t6_conc": "Conclusion",
        "t6_conc_text": "Kapanadze’s algebraic–geometric approach creates a natural conceptual bridge to Cauchy’s limit formalism. Here, the derivative is not defined directly by a limit formula; it is obtained through a geometrically and algebraically justified construction, while the limit interpretation serves as the analytical formalization of this construction.",
        
        # Tab 7
        "t7_header": "Limits",
        "t7_info": "Kapanadze’s algebraic–geometric approach.",
        "t7_intro_main": "This subsection considers functions for which the algebraic criterion of division by the square of the increment yields specific outcomes and clearly reveals the limits of method applicability.",
        "select_case": "Case",
        "case_options": ["|x| (modulus at 0)", "|x|^1.5 (lower smoothness)", "x^2 * sin(1/x) (oscillation)"],
        "case_abs_title": "Modulus Function at Point $x=0$",
        "case_abs_text": "At point $x=0$, the function graph has two different tangent lines: from the left side, the slope coefficient equals $-1$, and from the right side, it equals $1$. Thus, uniqueness of the tangent line is violated at this point, which does not satisfy the necessary condition for the existence of a derivative.",
        "t7_alg_interp_title": "Algebraic Interpretation",
        "t7_alg_interp_text": "According to Kapanadze’s algebraic criterion, existence of the derivative is connected to the condition that the difference between the function and the corresponding linear approximation is an infinitesimal quantity of second order. For the function $f(x)=|x|$, this condition is not satisfied at point $x=0$, because the behavior of the remainder differs from the left and right sides.",
        "t7_conc_title": "Conclusion",
        "t7_conc_text": "In this special case, Kapanadze’s algebraic criterion clearly indicates that the derivative does not exist. This example confirms that the method is effective not only for determining the existence of a derivative, but also for diagnosing its non-existence.",
        "case_1_text": "The function has a derivative, but the remainder does not decrease fast enough.",
        "case_2_text": "The function oscillates too rapidly, causing the remainder not to stabilize.",
        "left_tan": "Left",
        "right_tan": "Right"
    }
}

# ==========================================
# ენის არჩევა
# ==========================================
is_english = st.sidebar.toggle("English", value=False)
txt = translations["EN"] if is_english else translations["KA"]

ROMAN_PREFIX_RE = re.compile(r"^\s*[IVXLCDM]+\.\s*")
DIV_TAG_RE = re.compile(r"</?div[^>]*>", re.IGNORECASE)


def strip_roman_prefix(label):
    return ROMAN_PREFIX_RE.sub("", str(label), count=1)


def sanitize_text(text):
    return DIV_TAG_RE.sub("", str(text)).strip()


def academic_box(text):
    cleaned = sanitize_text(text)
    quoted = "\n".join([f"> {line}" if line.strip() else ">" for line in cleaned.splitlines()])
    st.markdown(quoted)

# ==========================================
# მათემატიკური ძრავა
# ==========================================
def algebraic_derivative(func_str, x0):
    x, k = sp.symbols('x k')
    try:
        f = sp.sympify(func_str)
        f_x0 = f.subs(x, x0)
        diff = f - (f_x0 + k * (x - x0))
        series = sp.series(diff, x, x0, n=2).removeO()
        linear_term = series.coeff(x - x0)
        solution = sp.solve(linear_term, k)
        if not solution:
            return None, None, "k not found"
        k_val = solution[0]
        tangent_eq = f_x0 + k_val * (x - x0)
        return f, k_val, tangent_eq
    except Exception as e:
        return None, None, str(e)

def solve_kapanadze_3d(func_str, x0_val, y0_val):
    x, y = sp.symbols('x y')
    kx, ky = sp.symbols('kx ky')
    try:
        func = sp.sympify(func_str)
        z0 = func.subs({x: x0_val, y: y0_val})
        kx_val = sp.diff(func, x).subs({x:x0_val, y:y0_val})
        ky_val = sp.diff(func, y).subs({x:x0_val, y:y0_val})
        return func, kx_val, ky_val, z0
    except Exception as e:
        return None, None, None, str(e)

# ==========================================
# ინტერფეისი
# ==========================================

# სათაური გადატანილია Sidebar-ში
st.sidebar.markdown(f"## {txt['title']}")
st.sidebar.markdown("---")
st.sidebar.title(txt["sidebar_title"])
nav_options_clean = [strip_roman_prefix(option) for option in txt["nav_options"]]
selected_nav = st.sidebar.radio("", nav_options_clean)
tab_selection = txt["nav_options"][nav_options_clean.index(selected_nav)]

# -----------------------------------------------------------------------------
# TAB 1: გეომეტრია
# -----------------------------------------------------------------------------
if tab_selection == txt["nav_options"][0]:
    st.header(txt["t1_header"])
    col1, col2 = st.columns([1, 2])
    with col1:
        academic_box(txt["t1_info"])
        st.latex(r"f(x)")
        func_input = st.text_input("", "x^2", key="geom_func")
        st.latex(r"A \text{ (Point)}")
        x_a = st.number_input("", value=1.0, step=0.1, format="%g", key="num_a")
        st.latex(r"h \text{ (Distance)}")
        h = st.slider("", 0.01, 2.0, 1.0, 0.01, format="%g", key="slider_h")
    with col2:
        x = sp.symbols('x')
        try:
            f = sp.sympify(func_input)
            f_lamb = sp.lambdify(x, f, 'numpy')
            xA, xB = x_a, x_a + h
            yA, yB = f_lamb(xA), f_lamb(xB)
            slope_secant = (yB - yA) / (xB - xA)
            slope_tangent = float(sp.diff(f, x).subs(x, xA))
            x_range = np.linspace(xA - 2, xB + 2, 500)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_range, y=f_lamb(x_range), name="f(x)", line=dict(color='#2196F3', width=3)))
            fig.add_trace(go.Scatter(x=x_range, y=yA + slope_secant * (x_range - xA), name=txt["secant"], line=dict(color='#FFC107', dash='dash')))
            fig.add_trace(go.Scatter(x=x_range, y=yA + slope_tangent * (x_range - xA), name=txt["tangent"], line=dict(color='#4CAF50', width=2)))
            fig.add_trace(go.Scatter(x=[xA, xB], y=[yA, yB], mode='markers+text', text=["A", "B"], marker=dict(size=12, color=['black', 'red'])))
            fig.update_layout(title=txt["viz_title"], height=500, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e: st.error(e)

# -----------------------------------------------------------------------------
# TAB 2: ალგებრული კალკულატორი
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][1]:
    st.header(txt["t2_header"])
    
    st.markdown(f"#### {sanitize_text(txt['t2_thm_title'])}")
    academic_box(txt["t2_thm_text"])
    
    st.latex(r"f(x) - [k(x-x_0) + f(x_0)] = (x-x_0)^2 \phi(x)")
    
    st.markdown(sanitize_text(txt["t2_thm_sub"]))

    col1, col2 = st.columns([1, 2])
    with col1:
        st.latex(r"f(x)")
        f_in = st.text_input("", "sin(x) * exp(0.5*x)", key="alg_func")
        st.latex(r"x_0")
        x0_in = st.number_input("", value=1.0, step=0.1, format="%g", key="num_x0")
        calc_btn = st.button(txt["calc_btn"], type="primary")
        
    if calc_btn:
        with col2:
            func_sym, k_res, tan_sym = algebraic_derivative(f_in, x0_in)
            if func_sym:
                st.markdown(f"**{txt['result']}:**")
                st.latex(rf"k = {float(k_res):.4f}")
                st.latex(rf"f'(x) = {sp.latex(k_res)}")
                st.latex(rf"y_{{\text{{tan}}}} = {sp.latex(tan_sym)}")
                
                x_range = np.linspace(x0_in - 2, x0_in + 2, 600)
                f_lamb, t_lamb = sp.lambdify('x', func_sym, 'numpy'), sp.lambdify('x', tan_sym, 'numpy')
                y_f, y_t = f_lamb(x_range), t_lamb(x_range)
                with np.errstate(divide='ignore', invalid='ignore'):
                    dx_vals = x_range - x0_in
                    remainder = (y_f - y_t) / (dx_vals**2)
                    remainder[np.abs(dx_vals) < 0.02] = np.nan
                
                fig = make_subplots(rows=2, cols=1, subplot_titles=(txt["vis_touch"], txt["proof_title"]))
                fig.add_trace(go.Scatter(x=x_range, y=y_f, name="f(x)", line=dict(color='#2196F3')), row=1, col=1)
                fig.add_trace(go.Scatter(x=x_range, y=y_t, name=txt["tangent"], line=dict(color='#FF5722', dash='dash')), row=1, col=1)
                fig.add_trace(go.Scatter(x=x_range, y=remainder, name=txt["residue"], line=dict(color='#4CAF50', width=2)), row=2, col=1)
                fig.update_layout(height=700, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
                st.success(txt["success_msg"])
            else: st.error(f"{txt['error_msg']}: {tan_sym}")

# -----------------------------------------------------------------------------
# TAB 3: ტოპოლოგია (3D)
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][2]:
    st.header(txt["t3_header"])
    
    st.markdown(sanitize_text(txt["t3_intro"]))
    st.latex(r"z = f(x,y),")
    st.markdown(sanitize_text(txt["t3_info"]))
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write(txt["surface_label"])
        st.latex(r"f(x,y)")
        f3_str = st.text_input("", "x^2 + y^2 - 0.5*x*y", key="3d_func")
        st.latex(r"(x_0, y_0)")
        x0 = st.number_input("x0", 0.0, format="%g")
        y0 = st.number_input("y0", 0.0, format="%g")
        btn_3d = st.button(txt["build_3d"], type="primary")
    if btn_3d:
        with col2:
            func_sym, kx, ky, z0 = solve_kapanadze_3d(f3_str, x0, y0)
            if func_sym:
                st.write(txt["found_partials"])
                st.latex(rf"k_x = {float(kx):.4f}, \quad k_y = {float(ky):.4f}")
                st.write(txt["t3_res_text"])
                
                x_v = np.linspace(x0-2, x0+2, 40)
                X, Y = np.meshgrid(x_v, x_v)
                x_sym, y_sym = sp.symbols('x y')
                Z = sp.lambdify((x_sym, y_sym), func_sym, 'numpy')(X, Y)
                Z_plane = float(z0) + float(kx)*(X-x0) + float(ky)*(Y-y0)
                fig = go.Figure()
                fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8, name=txt["surface"]))
                fig.add_trace(go.Surface(z=Z_plane, x=X, y=Y, colorscale=[[0,'red'],[1,'red']], opacity=0.5, showscale=False, name=txt["tan_plane"]))
                fig.add_trace(go.Scatter3d(x=[x0], y=[y0], z=[float(z0)], mode='markers', marker=dict(size=5, color='black')))
                fig.update_layout(height=700, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: ტრიგონომეტრია
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][3]:
    st.header(txt["t4_header"])
    
    academic_box(txt["t4_intro_long"])
    
    trig_mode = st.radio(txt["trig_mode_select"], [txt["trig_standard"], txt["trig_inverse"]], horizontal=True)
    
    col1, col2 = st.columns([1, 2])
    
    if trig_mode == txt["trig_standard"]:
        with col1:
            st.latex(r"\theta \text{ (rad)}")
            angle = st.slider("", 0.0, 2*np.pi, 1.0, 0.1, format="%g")
            st.latex(rf"\sin(t) \approx {np.sin(angle):.2f}")
            st.latex(rf"\cos(t) \approx {np.cos(angle):.2f}")
        with col2:
            t_vals = np.linspace(0, 2*np.pi, 100)
            circle_x, circle_y = np.cos(t_vals), np.sin(t_vals)
            P_x, P_y = np.cos(angle), np.sin(angle)
            tan_x = [P_x - 0.5*(-P_y), P_x + 0.5*(-P_y)]
            tan_y = [P_y - 0.5*(P_x), P_y + 0.5*(P_x)]
            fig = make_subplots(rows=1, cols=2, subplot_titles=(txt["unit_circle"], "y = sin(x)"))
            fig.add_trace(go.Scatter(x=circle_x, y=circle_y, line=dict(color='black')), row=1, col=1)
            fig.add_trace(go.Scatter(x=tan_x, y=tan_y, line=dict(color='red', width=3)), row=1, col=1)
            fig.add_trace(go.Scatter(x=[P_x], y=[P_y], mode='markers', marker=dict(color='blue', size=10)), row=1, col=1)
            fig.add_trace(go.Scatter(x=t_vals, y=np.sin(t_vals), line=dict(color='blue')), row=1, col=2)
            slope_x = np.linspace(angle-0.5, angle+0.5, 10)
            slope_y = np.sin(angle) + np.cos(angle)*(slope_x-angle)
            fig.add_trace(go.Scatter(x=slope_x, y=slope_y, line=dict(color='red', width=3)), row=1, col=2)
            fig.add_trace(go.Scatter(x=[angle], y=[np.sin(angle)], mode='markers', marker=dict(color='blue', size=10)), row=1, col=2)
            fig.update_layout(height=600, width=800, showlegend=False, template="plotly_white")
            fig.update_xaxes(range=[-1.5, 1.5], row=1, col=1)
            fig.update_yaxes(scaleanchor="x", scaleratio=1, range=[-1.5, 1.5], row=1, col=1)
            st.plotly_chart(fig, use_container_width=True)
    else:
        academic_box(txt["inv_info"])
        with col1:
            st.latex(r"x \in [-1, 1]")
            val = st.slider("", -1.0, 1.0, 0.5, 0.01, format="%g")
            val_tan = val * 5 
            angle_asin = np.arcsin(val)
            angle_acos = np.arccos(val)
            angle_atan = np.arctan(val_tan)
            
            st.markdown(f"**{txt['inv_res']}:**")
            st.latex(rf"\arcsin(0.5) \approx 30.0^\circ")
            st.latex(rf"\arccos(0.5) \approx 60.0^\circ")
            st.latex(rf"\arctan(2.5) \approx 68.2^\circ")
            st.write("---")
            st.latex(rf"\arcsin({val}) = {angle_asin:.2f} \text{{ rad}} \approx {np.degrees(angle_asin):.1f}^\circ")
            st.latex(rf"\arccos({val}) = {angle_acos:.2f} \text{{ rad}} \approx {np.degrees(angle_acos):.1f}^\circ")
            st.latex(rf"\arctan({val_tan:.1f}) = {angle_atan:.2f} \text{{ rad}} \approx {np.degrees(angle_atan):.1f}^\circ")

        with col2:
            x_domain = np.linspace(-1, 1, 100)
            x_tan_domain = np.linspace(-5, 5, 100)
            fig = make_subplots(rows=3, cols=1, subplot_titles=("y = arcsin(x)", "y = arccos(x)", "y = arctan(x)"), vertical_spacing=0.1)
            fig.add_trace(go.Scatter(x=x_domain, y=np.arcsin(x_domain), line=dict(color='blue')), row=1, col=1)
            fig.add_trace(go.Scatter(x=[val], y=[angle_asin], mode='markers', marker=dict(color='red', size=10)), row=1, col=1)
            fig.add_trace(go.Scatter(x=x_domain, y=np.arccos(x_domain), line=dict(color='green')), row=2, col=1)
            fig.add_trace(go.Scatter(x=[val], y=[angle_acos], mode='markers', marker=dict(color='red', size=10)), row=2, col=1)
            fig.add_trace(go.Scatter(x=x_tan_domain, y=np.arctan(x_tan_domain), line=dict(color='purple')), row=3, col=1)
            fig.add_trace(go.Scatter(x=[val_tan], y=[angle_atan], mode='markers', marker=dict(color='red', size=10)), row=3, col=1)
            fig.update_layout(height=800, showlegend=False, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
    # დასკვნა ბოლოში
    st.markdown("---")
    st.subheader(txt["t4_conc"])
    academic_box(txt["t4_conc_text"])

# -----------------------------------------------------------------------------
# TAB 5: მაჩვენებლიანი და ლოგარითმული
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][4]:
    st.header(txt["t5_header"])
    academic_box(txt["t5_intro"])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        func_mode = st.radio(txt["t5_select_mode"], ["Exponential (e^x)", "Logarithmic (log)"], horizontal=True)
        
        if "Exponential" in func_mode:
            st.markdown(f"{txt['t5_exp_desc']}")
            st.latex(r"f(x) = e^x")
            
            st.markdown("**შეხების წერტილი:**")
            st.latex(r"x_0")
            x0_exp = st.number_input("", value=1.0, step=0.1, format="%g", key="x0_exp")
            val = np.exp(x0_exp)
            slope = val
            
            st.markdown("**მიღებული შედეგი:**")
            st.latex(rf"f(x_0) = e^{{{x0_exp}}} \approx {val:.4f}")
            st.latex(rf"f'(x_0) = e^{{{x0_exp}}} \approx {slope:.4f}")
            st.info(txt['value_eq_slope'])
            
            x_range = np.linspace(x0_exp - 2, x0_exp + 2, 100)
            y_exp = np.exp(x_range)
            y_tan = val + slope * (x_range - x0_exp)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_range, y=y_exp, name="e^x", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=x_range, y=y_tan, name=txt["tangent"], line=dict(color='red', dash='dash')))
            fig.add_trace(go.Scatter(x=[x0_exp], y=[val], mode='markers+text', text=["P"], textposition="top left", marker=dict(size=12, color='black')))
            fig.update_layout(title=r"$y = e^x$", height=500, template="plotly_white")
            
            with col2:
                st.plotly_chart(fig, use_container_width=True, key="chart_exp")
            
        else:
            st.markdown(f"{txt['t5_log_desc']}")
            st.latex(r"f'(x) = \frac{1}{x \ln(a)}")
            
            st.write(txt['base_select'])
            base_type = st.selectbox("", txt["bases"])
            
            st.markdown("**განხილული წერტილი:**")
            st.latex(r"x_0 (>0)")
            x0_log = st.number_input("", value=1.0, step=0.1, min_value=0.01, format="%g", key="x0_log")
            
            if "e" in base_type:
                log_func_str, display_str = "log(x)", "ln(x)"
            elif "10" in base_type:
                log_func_str, display_str = "log(x, 10)", "log_{10}(x)"
            else:
                log_func_str, display_str = "log(x, 2)", "log_{2}(x)"
            
            if st.button(txt["calc_log"], type="primary"):
                func_sym, k_res, tan_sym = algebraic_derivative(log_func_str, x0_log)
                if func_sym:
                    st.markdown("**შედეგი:**")
                    st.latex(f"f'({x0_log}) = {sp.latex(k_res)}")
                    
                    x_start = max(0.01, x0_log - 2)
                    x_range = np.linspace(x_start, x0_log + 2, 500)
                    f_lamb = sp.lambdify('x', func_sym, 'numpy')
                    t_lamb = sp.lambdify('x', tan_sym, 'numpy')
                    y_f, y_t = f_lamb(x_range), t_lamb(x_range)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x_range, y=y_f, name=display_str, line=dict(color='purple')))
                    fig.add_trace(go.Scatter(x=x_range, y=y_t, name=txt["tangent"], line=dict(color='orange', dash='dash')))
                    fig.add_trace(go.Scatter(x=[x0_log], y=[f_lamb(x0_log)], mode='markers', marker=dict(color='black', size=10)))
                    fig.update_layout(title=f"Graph: {display_str}", height=500, template="plotly_white")
                    
                    with col2:
                        st.plotly_chart(fig, use_container_width=True, key="chart_log")
                else:
                    st.error("Error")
    
    # დასკვნა ბოლოში
    st.markdown("---")
    st.subheader(txt["t5_conc"])
    academic_box(txt["t5_conc_text"])

# -----------------------------------------------------------------------------
# TAB 6: კავშირი ნიუტონთან და კოშისთან (+ ფიზიკა ქვეთავი)
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][5]:
    st.header(txt["t6_header"])
    academic_box(txt["t6_intro"])
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(txt["t6_sec_incr"])
        st.write(txt["t6_fixed"])
        st.latex(r"x_0")
        x0 = st.number_input("", value=1.0, step=0.1, format="%g", key="nc_x0")
        st.write(txt["t6_arg_incr"])
        st.latex(r"\Delta x")
        dx = st.slider("", 0.01, 2.0, 1.0, 0.01, format="%g", key="nc_dx")
        
        x = sp.symbols('x')
        f = sp.sympify("x^2")
        f_lamb = sp.lambdify(x, f, 'numpy')
        y0 = f_lamb(x0)
        y_next = f_lamb(x0 + dx)
        delta_F = y_next - y0
        k = float(sp.diff(f, x).subs(x, x0))
        dF = k * dx
        diff_val = delta_F - dF
        
        st.write(txt["t6_func_incr"])
        st.latex(r"\Delta F")
        st.write(txt["t6_geom_bc"])
        st.latex(rf"{delta_F:.4f}")
        
        st.write(txt["t6_diff"])
        st.latex(r"dF")
        st.write(txt["t6_geom_bn"])
        st.latex(rf"{dF:.4f}")
        
        st.write(txt["t6_rem"])
        st.latex(r"\Delta F - dF")
        st.write(txt["t6_geom_nc"])
        st.latex(rf"{diff_val:.4f}")
        
        st.markdown("---")
        st.subheader(txt["t6_sec_alg"])
        st.markdown(sanitize_text(txt["t6_alg_text"]))

    with col2:
        x_range = np.linspace(max(0, x0 - 0.5), x0 + dx + 0.5, 100)
        y_curve = f_lamb(x_range)
        y_tan = y0 + k * (x_range - x0)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_range, y=y_curve, name="F(x)", line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=x_range, y=y_tan, name="Tangent", line=dict(color='red', dash='dash')))
        
        pt_A, pt_B = [x0, y0], [x0 + dx, y0]
        pt_C, pt_N = [x0 + dx, y_next], [x0 + dx, y0 + dF]
        pt_D, pt_x0_ax = [x0 + dx, 0], [x0, 0]

        fig.add_trace(go.Scatter(x=[pt_A[0], pt_B[0]], y=[pt_A[1], pt_B[1]], mode='lines', line=dict(color='black', dash='dot'), name="Δx (AB)"))
        fig.add_trace(go.Scatter(x=[pt_B[0], pt_C[0]], y=[pt_B[1], pt_C[1]], mode='lines', line=dict(color='black'), name="ΔF (BC)"))
        fig.add_trace(go.Scatter(x=[pt_C[0], pt_D[0]], y=[pt_C[1], pt_D[1]], mode='lines', line=dict(color='gray', dash='dash', width=1), showlegend=False))
        fig.add_trace(go.Scatter(x=[pt_A[0], pt_x0_ax[0]], y=[pt_A[1], pt_x0_ax[1]], mode='lines', line=dict(color='gray', dash='dash', width=1), showlegend=False))

        labels, x_coords, y_coords = ["A", "B", "C", "N", "D"], [pt_A[0], pt_B[0], pt_C[0], pt_N[0], pt_D[0]], [pt_A[1], pt_B[1], pt_C[1], pt_N[1], pt_D[1]]
        text_pos = ["top left", "bottom right", "top right", "top left", "bottom right"]
        fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='markers+text', text=labels, textposition=text_pos, marker=dict(size=10, color='black'), name="Points"))

        fig.add_annotation(x=x0 + dx, y=(y0 + y0 + dF)/2, text="dF", showarrow=False, xshift=15, font=dict(color="green"))
        fig.add_annotation(x=x0 + dx, y=(y0 + y_next)/2, text="ΔF", showarrow=False, xshift=35, font=dict(color="blue"))
        fig.add_annotation(x=(x0 + x0 + dx)/2, y=y0, text="Δx", showarrow=False, yshift=-15)
        fig.add_annotation(x=x0, y=0, text="x₀", showarrow=False, yshift=-15)
        fig.add_annotation(x=x0 + dx, y=0, text="x₀ + Δx", showarrow=False, yshift=-15)
        fig.add_hline(y=0, line_color="black", line_width=1)

        fig.update_layout(title="Newton-Cauchy Connection (Geometry)", height=600, xaxis_title="X", yaxis_title="Y", showlegend=False, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    # --- ფიზიკური ინტერპრეტაცია (ქვეთავი) ---
    st.markdown("---")
    st.subheader(txt["t8_header"])
    academic_box(txt["t8_info"])
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write(txt['time'])
        t = st.slider("", 0.0, 2.0, 0.5, 0.05, format="%g", key="phys_time")
        x_val = t
        y_val = -(t**2) + 2
        vy = -2 * t
        st.markdown(f"**{txt['velocity_vec']}:**")
        st.latex(rf"(1, {vy:.2f})")
        
    with col2:
        t_range = np.linspace(0, 2, 100)
        x_traj = t_range
        y_traj = -(t_range**2) + 2
        slope = vy / 1
        x_tan = np.linspace(x_val, x_val + 0.5, 10)
        y_tan = y_val + slope * (x_tan - x_val)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_traj, y=y_traj, name=txt["trajectory"], line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=[x_val], y=[y_val], mode='markers', marker=dict(size=15, color='black'), name=txt["body"]))
        fig.add_trace(go.Scatter(x=x_tan, y=y_tan, name=txt["inertia"], line=dict(color='red', width=3), mode='lines+markers', marker=dict(symbol='arrow', size=10)))
        fig.add_trace(go.Scatter(x=[0, 2], y=[-2, -2], line=dict(color='green', width=5), name=txt["ground"]))
        fig.update_layout(title=txt["ballistic"], height=500, yaxis=dict(range=[-2.5, 2.5], scaleanchor="x", scaleratio=1), template="plotly_white")
        st.plotly_chart(fig, use_container_width=True, key="phys_chart")
    
    # დასკვნა ბოლოში
    st.markdown("---")
    st.subheader(txt["t6_conc"])
    academic_box(txt["t6_conc_text"])

# -----------------------------------------------------------------------------
# TAB 7: განსაკუთრებული შემთხვევები
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][6]:
    st.header(txt["t7_header"])
    academic_box(txt["t7_info"])
    
    st.markdown(sanitize_text(txt["t7_intro_main"]))
    
    col1, col2 = st.columns([1, 2])
    with col1:
        problem_label = st.selectbox(f"{txt['select_case']}:", txt["case_options"])
        
        if "Absolute" in problem_label or "მოდული" in problem_label:
            st.subheader(txt["case_abs_title"])
            st.markdown(txt["case_abs_text"])
            
            st.subheader(txt["t7_alg_interp_title"])
            st.markdown(txt["t7_alg_interp_text"])
            
            problem_type = "abs"
        elif "1.5" in problem_label:
            st.markdown(txt["case_1_text"])
            problem_type = "1.5"
        else:
            st.markdown(txt["case_2_text"])
            problem_type = "osc"
            
    with col2:
        x = np.linspace(-1, 1, 1000)
        if problem_type == "abs":
            y = np.abs(x)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, name="|x|", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], name=txt["right_tan"] + " (k=1)", line=dict(color='green', dash='dash')))
            fig.add_trace(go.Scatter(x=[-1, 0], y=[1, 0], name=txt["left_tan"] + " (k=-1)", line=dict(color='red', dash='dash')))
            fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=12, color='black'), name='Point (0,0)'))
            fig.update_layout(title="y = |x| Corner Point", height=500, template="plotly_white")
        elif problem_type == "1.5":
            x_pos, x_neg = np.linspace(0, 1, 500), np.linspace(-1, 0, 500)
            y_pos, y_neg = x_pos**1.5, np.abs(x_neg)**1.5
            x_all = np.concatenate([x_neg, x_pos])
            y_all = np.concatenate([y_neg, y_pos])
            tangent = np.zeros_like(x_all)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_all, y=y_all, name="|x|^1.5", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=x_all, y=tangent, name=txt["tangent"], line=dict(color='red', dash='dash')))
            with np.errstate(divide='ignore', invalid='ignore'): remainder = y_all / (x_all**2)
            fig.add_trace(go.Scatter(x=x_all, y=remainder, name=txt["residue"], line=dict(color='purple')))
            fig.update_layout(title="Analysis", height=600, yaxis=dict(range=[0, 5]), template="plotly_white")
        else: # Oscillation
            y = (x**2) * np.sin(1/(x + 1e-9))
            tangent = np.zeros_like(x)
            with np.errstate(divide='ignore', invalid='ignore'): remainder = np.sin(1/(x + 1e-9))
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, name="f(x)", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=x, y=remainder, name=txt["residue"], line=dict(color='purple')))
            fig.update_layout(title="Oscillation", height=600, yaxis=dict(range=[-2, 2]), template="plotly_white")

        st.plotly_chart(fig, use_container_width=True)
    
    # დასკვნა ბოლოში
    st.markdown("---")
    st.subheader(txt["t7_conc_title"])
    academic_box(txt["t7_conc_text"])
