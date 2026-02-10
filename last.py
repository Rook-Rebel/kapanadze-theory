import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    /* ფონტების და ფერების აკადემიური სტილი */
    h1 { 
        font-size: 2.0rem !important; 
        font-weight: 600 !important; 
        font-family: 'Times New Roman', Times, serif; 
        color: #2c3e50;
    }
    h2, h3, h4 { 
        font-family: 'Times New Roman', Times, serif; 
        color: #34495e;
    }
    
    /* ტექსტური ბლოკები */
    .academic-box {
        padding: 20px;
        border-radius: 5px;
        background-color: #f8f9fa; /* ღია ნაცრისფერი/თეთრი */
        border-left: 4px solid #2c3e50; /* მუქი ლურჯი */
        margin-bottom: 20px;
        font-family: 'Georgia', serif;
        color: #212529;
        line-height: 1.6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    /* ღილაკების სტილი */
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- თარგმანების ლექსიკონი (ნუმერაციის გარეშე) ---
translations = {
    "KA": {
        "sidebar_title": "სარჩევი",
        "nav_options": [
            "გეომეტრიული არსი",
            "ალგებრული კრიტერიუმი",
            "სივრცითი (ტოპოლოგიური) განზოგადება",
            "ტრიგონომეტრიული ანალიზი",
            "მაჩვენებლიანი და ლოგარითმული",
            "კავშირი ნიუტონთან და კოშისთან",
            "მეთოდის გამოყენების საზღვრები"
        ],
        "title": "ინტერაქტიული მოდელი წარმოებულის გეომეტრიული და ალგებრული ინტერპრეტაციისათვის",
        "bases": ["e (ნატურალური ln)", "10 (ათობითი)", "2 (ორობითი)"],
        
        # Tab 1
        "t1_header": "მკვეთი წრფის თანმიმდევრული მიახლოება შემხებ წრფასთან",
        "t1_info": "შემხები წრფა განისაზღვრება როგორც მკვეთი წრფის ლიმიტური შემთხვევა, როდესაც მეორე წერტილი თანმიმდევრულად უახლოვდება ფიქსირებულ წერტილს ფუნქციის გრაფიკზე.",
        "func_label": "ფუნქცია f(x)",
        "point_a": "ფიქსირებული წერტილი (A)",
        "point_b_dist": "მეორე წერტილის დაშორება (h)",
        "secant": "მკვეთი წრფე",
        "tangent": "შემხები წრფე",
        "viz_title": "გეომეტრიული ვიზუალიზაცია",
        
        # Tab 2
        "t2_header": "ნაშთის კვადრატზე გაყოფის ალგებრული მეთოდი",
        "t2_thm_title": "ალგებრული კრიტერიუმი შემხები წრფისათვის",
        "t2_thm_text": "წრფე $y = k(x-x_0) + f(x_0)$ არის ფუნქციის $f(x)$ შემხები წრფე წერტილში $x_0$ მაშინ და მხოლოდ მაშინ, როდესაც ფუნქციისა და აღნიშნული წრფის სხვაობა იყოფა $(x-x_0)^2$-ზე. ანუ, არსებობს ისეთი ფუნქცია $\phi(x)$, რომ: $$f(x) - [k(x-x_0) + f(x_0)] = (x-x_0)^2 \phi(x)$$",
        "t2_thm_sub": "ეს პირობა ნიშნავს, რომ ფუნქციისა და მისი შემხები წრფის სხვაობა $x_0$-ის მახლობლად არის მეორე რიგის უსასრულოდ მცირე სიდიდე. შესაბამისად, ნაშთის გრაფიკი არ ავლენს უსასრულოდ ზრდად ქცევას შეხების წერტილის მახლობლად.",
        "touch_point": "შეხების წერტილი x0",
        "calc_btn": "გამოთვლა და ანალიზი",
        "result": "შედეგი",
        "slope_found": "დახრილობის კოეფიციენტი (k)",
        "tan_eq": "შემხები წრფის განტოლება",
        "proof_title": "ნაშთის ანალიზი: R(x) / (x-x0)²",
        "vis_touch": "ფუნქცია და შემხები",
        "residue": "ნაშთი (Remainder)",
        "success_msg": "✔ კრიტერიუმი შესრულდა: ნაშთი არის სასრული (მეორე რიგის მცირე).",
        "error_msg": "შეცდომა",
        
        # Tab 3
        "t3_header": "კაპანაძის მიდგომის სივრცითი (ტოპოლოგიური) განზოგადება",
        "t3_info": "სამგანზომილებიან სივრცეში შემხები სიბრტყე განისაზღვრება იმ პირობით, რომ ფუნქციისა და სიბრტყის სხვაობა მოცემული წერტილის მახლობლად არის მეორე რიგის უსასრულოდ მცირე სიდიდე. ეს მიდგომა იძლევა ტოპოლოგიურ–გეომეტრიულ ინტერპრეტაციას, რომელიც არ საჭიროებს ზღვრის ცნების საწყის ეტაპზე გამოყენებას.",
        "surface_label": "ზედაპირი z = f(x,y)",
        "build_3d": "3D მოდელის აგება",
        "found_partials": "ნაპოვნი კოეფიციენტები",
        "surface": "ზედაპირი",
        "tan_plane": "შემხები სიბრტყე",
        
        # Tab 4
        "t4_header": "ტრიგონომეტრიული ფუნქციების გეომეტრიულ–ალგებრული ანალიზი",
        "t4_info": "წარმოდგენილი მიდგომა ეფუძნება ტრიგონომეტრიული ფუნქციების წარმოებულების გეომეტრიულ და ალგებრულ ინტერპრეტაციას. ანალიზი ხორციელდება ერთეულოვან წრეწირზე მოძრაობის გეომეტრიული მოდელის გამოყენებით. ტრიგონომეტრიული ფუნქციების ეს გეომეტრიულ–ალგებრული წარმოდგენა ბუნებრივად უკავშირებს ერთეულოვან წრეწირს, ფუნქციის ცვლილების სიჩქარესა და წარმოებულის ცნებას.",
        "angle": "კუთხე (რადიანებში)",
        "slope": "დახრილობა (cos)",
        "unit_circle": "ერთეულოვანი წრეწირი",
        "trig_mode_select": "ვიზუალიზაციის რეჟიმი",
        "trig_standard": "ტრიგონომეტრიული წრეწირი (sin/cos)",
        "trig_inverse": "შებრუნებული ფუნქციები (arcsin/arccos/arctan)",
        "input_val": "არგუმენტის მნიშვნელობა (x)",
        "inv_res": "შედეგები (კუთხეები)",
        "inv_info": "შებრუნებული ტრიგონომეტრიული ფუნქციების ეს გეომეტრიულ–ალგებრული წარმოდგენა უზრუნველყოფს წარმოებულის ცნების კონცეპტუალურ გააზრებას მოძრაობის, დახრილობისა და ფუნქციური დამოკიდებულების საფუძველზე.",
        
        # Tab 5
        "t5_header": "მაჩვენებლიანი და ლოგარითმული ფუნქციების გეომეტრიულ–ალგებრული ანალიზი",
        "t5_intro": "მოცემულ თავში განიხილება მაჩვენებლიანი და ლოგარითმული ფუნქციები კაპანაძის გეომეტრიულ–ალგებრული მიდგომის ფარგლებში.",
        "t5_select_mode": "ფუნქციის ტიპი",
        "t5_exp_info": "მაჩვენებლიანი ფუნქცია $e^x$ გამოირჩევა განსაკუთრებული თვისებით: მისი წარმოებული ყველა წერტილში ტოლია თავად ფუნქციის მნიშვნელობისა. $f'(x) = e^x$. ეს ფაქტი წარმოადგენს მაჩვენებლიანი ფუნქციის ფუნდამენტურ გეომეტრიულ თვისებას.",
        "t5_log_info": "კაპანაძის მეთოდის მიხედვით, ლოგარითმული ფუნქციის $f(x) = \log_a(x)$ წარმოებული მიიღება ალგებრული კრიტერიუმის გამოყენებით: $f'(x) = \\frac{1}{x \\ln(a)}$.",
        "value_eq_slope": "ფუნქციის მნიშვნელობა და დახრის კოეფიციენტი ემთხვევა.",
        "base_select": "აირჩიეთ ფუძე",
        "calc_log": "ანალიზი",
        "residue_analysis": "ნაშთის ქცევა",
        "graph": "გრაფიკი",
        
        # Tab 6 (Newton + Physics)
        "t6_header": "კავშირი ნიუტონისა და კოშის კლასიკურ მიდგომებთან",
        "t6_info": "მოცემულ თავში განიხილება კაპანაძის ალგებრული–გეომეტრიული მიდგომის კავშირი ნიუტონისა და კოშის მიერ ჩამოყალიბებულ კლასიკურ კონცეფციებთან. წარმოდგენილი მეთოდი არ ეწინააღმდეგება კლასიკურ ანალიზს; პირიქით, იგი წარმოადგენს ალტერნატიულ გზას. კაპანაძის მიდგომაში წარმოებული განიხილება როგორც **ზღვრული გეომეტრიული ობიექტი** — შემხები წრფე.",
        "delta_x_label": "არგუმენტის ნაზრდი (Δx)",
        "delta_f": "ფუნქციის ნაზრდი (ΔF)",
        "d_f": "დიფერენციალი (dF)",
        "diff_val": "სხვაობა (NC = ΔF - dF)",
        "kapanadze_limit_text": "თუ სხვაობა $\Delta F - dF$ არგუმენტის ნაზრდის შემცირებისას მცირდება ისე, რომ აკმაყოფილებს კაპანაძის ალგებრულ კრიტერიუმს (წარმოადგენს მეორე რიგის უსასრულოდ მცირე სიდიდეს), მაშინ შემხები წრფე მიიღება როგორც ზღვრული ობიექტი.",
        
        "t8_header": "ფიზიკური ინტერპრეტაცია (კინემატიკა)",
        "t8_info": "ფიზიკურ კონტექსტში, შემხები წრფე (წარმოებული) წარმოადგენს სხეულის მომენტალურ სიჩქარეს ან ტრაექტორიას, რომელსაც სხეული გაყვებოდა, მასზე მოქმედი ძალები რომ უცებ გამქრალიყო (ინერციით მოძრაობა).",
        "time": "დრო (t)",
        "velocity_vec": "სიჩქარის ვექტორი",
        "trajectory": "ტრაექტორია",
        "body": "სხეული",
        "inertia": "ინერცია (შემხები)",
        "ground": "ზედაპირი",
        "ballistic": "ბალისტიკური მოძრაობის სიმულაცია",

        # Tab 7
        "t7_header": "მეთოდის გამოყენების საზღვრები (განსაკუთრებული შემთხვევები)",
        "t7_info": "წარმოდგენილ ქვეთავში განიხილება ისეთი ფუნქციები, რომელთა შემთხვევაში ნაშთის კვადრატზე გაყოფის ალგებრული კრიტერიუმი იძლევა სპეციფიკურ შედეგს და ნათლად ავლენს მეთოდის გამოყენების საზღვრებს.",
        "select_case": "აირჩიეთ შემთხვევა",
        "case_options": ["|x| (მოდული 0-ში)", "|x|^1.5 (ნაკლები სიგლუვე)", "x^2 * sin(1/x) (ოსცილაცია)"],
        "case_abs_text": "წერტილში $x=0$ ფუნქციას $f(x)=|x|$ გააჩნია ორი განსხვავებული შემხები წრფე (მარცხნიდან $k=-1$, მარჯვნიდან $k=1$). ამგვარად, მოცემულ წერტილში შემხები წრფის უნიკალურობა ირღვევა.",
        "case_1_text": "ფუნქციას აქვს წარმოებული, მაგრამ ნაშთი არ მცირდება საკმარისად სწრაფად.",
        "case_2_text": "ფუნქცია ირხევა ძალიან სწრაფად, რის გამოც ნაშთი არ სტაბილურდება.",
        "conclusion": "მოცემულ განსაკუთრებულ შემთხვევაში კაპანაძის ალგებრული კრიტერიუმი ცალსახად მიუთითებს, რომ წარმოებული არ არსებობს.",
        "left_tan": "მარცხენა შემხები",
        "right_tan": "მარჯვენა შემხები"
    },
    "EN": {
        "sidebar_title": "Contents",
        "nav_options": [
            "Geometric Essence",
            "Algebraic Criterion",
            "Spatial Generalization (3D)",
            "Trigonometric Analysis",
            "Exponential & Logarithmic",
            "Connection with Newton & Cauchy",
            "Limits of Applicability"
        ],
        "title": "Interactive Model for Geometric and Algebraic Interpretation of the Derivative",
        "bases": ["e (Natural ln)", "10 (Decimal)", "2 (Binary)"],
        "t1_header": "Successive Approximation of the Secant to the Tangent",
        "t1_info": "The tangent line is defined as the limiting case of the secant line when the second point successively approaches a fixed point on the function graph.",
        "func_label": "Function f(x)",
        "point_a": "Fixed Point (A)",
        "point_b_dist": "Distance to Second Point (h)",
        "secant": "Secant Line",
        "tangent": "Tangent Line",
        "viz_title": "Geometric Visualization",
        "t2_header": "Algebraic Method of Dividing Remainder by Square",
        "t2_thm_title": "Algebraic Criterion for the Tangent Line",
        "t2_thm_text": "The line $y = k(x-x_0) + f(x_0)$ is the tangent to $f(x)$ at $x_0$ if and only if the difference represents an infinitesimal of the second order. $$f(x) - [k(x-x_0) + f(x_0)] = (x-x_0)^2 \phi(x)$$",
        "t2_thm_sub": "This condition implies that the graph of the remainder does not exhibit infinite growth near the point of tangency.",
        "touch_point": "Point of Tangency x0",
        "calc_btn": "Calculate and Analyze",
        "result": "Result",
        "slope_found": "Slope Coefficient (k)",
        "tan_eq": "Tangent Equation",
        "proof_title": "Remainder Analysis: R(x) / (x-x0)²",
        "vis_touch": "Function and Tangent",
        "residue": "Remainder",
        "success_msg": "✔ Criterion met: Remainder is finite (second order infinitesimal).",
        "error_msg": "Error",
        "t3_header": "Spatial (Topological) Generalization",
        "t3_info": "In 3D space, the tangent plane is defined by the condition that the difference between the function and the plane is an infinitesimal of the second order near the given point.",
        "surface_label": "Surface z = f(x,y)",
        "build_3d": "Build 3D Model",
        "found_partials": "Found Coefficients",
        "surface": "Surface",
        "tan_plane": "Tangent Plane",
        "t4_header": "Geometric-Algebraic Analysis of Trigonometric Functions",
        "t4_info": "The presented approach is based on the geometric and algebraic interpretation of derivatives of trigonometric functions using the unit circle model.",
        "angle": "Angle (radians)",
        "slope": "Slope (cos)",
        "unit_circle": "Unit Circle",
        "trig_mode_select": "Visualization Mode",
        "trig_standard": "Trigonometric Circle (sin/cos)",
        "trig_inverse": "Inverse Functions (arcsin/arccos/arctan)",
        "input_val": "Argument Value (x)",
        "inv_res": "Results (Angles)",
        "inv_info": "This geometric-algebraic representation of inverse trigonometric functions ensures a conceptual understanding of the derivative based on motion, slope, and functional dependence.",
        "t5_header": "Analysis of Exponential and Logarithmic Functions",
        "t5_intro": "This chapter examines exponential and logarithmic functions within the framework of Kapanadze's geometric-algebraic approach.",
        "t5_select_mode": "Function Type",
        "t5_exp_info": "The exponential function $e^x$ is distinguished by the property that its derivative at any point equals the function value itself.",
        "t5_log_info": "For the logarithmic function $f(x) = \log_a(x)$, the derivative is obtained via the algebraic criterion.",
        "value_eq_slope": "Function value and slope coefficient coincide.",
        "base_select": "Select Base",
        "calc_log": "Analyze",
        "residue_analysis": "Remainder Behavior",
        "graph": "Graph",
        "t6_header": "Connection with Classical Approaches of Newton and Cauchy",
        "t6_info": "This chapter discusses the connection of Kapanadze's approach with the concepts of Newton and Cauchy. Here, the derivative is viewed as a **limiting geometric object** — the tangent line.",
        "delta_x_label": "Argument Increment (Δx)",
        "delta_f": "Function Increment (ΔF = BC)",
        "d_f": "Differential (dF = BN)",
        "diff_val": "Difference (NC = ΔF - dF)",
        "kapanadze_limit_text": "If the difference $\Delta F - dF$ decreases such that it satisfies the algebraic criterion, the tangent line is obtained as a limiting object.",
        "t8_header": "Physical Interpretation (Kinematics)",
        "t8_info": "In a physical context, the tangent line (derivative) represents the instantaneous velocity of a body, or the trajectory the body would follow if forces acting on it suddenly vanished (inertial motion).",
        "time": "Time (t)",
        "velocity_vec": "Velocity Vector",
        "trajectory": "Trajectory",
        "body": "Body",
        "inertia": "Inertia (Tangent)",
        "ground": "Ground",
        "ballistic": "Ballistic Motion Simulation",
        "t7_header": "Limits of Applicability (Special Cases)",
        "t7_info": "We examine functions where the algebraic criterion yields specific results, revealing the boundaries of the method.",
        "select_case": "Select Case",
        "case_options": ["|x| (Absolute Value at 0)", "|x|^1.5 (Less Smoothness)", "x^2 * sin(1/x) (Oscillation)"],
        "case_abs_text": "At $x=0$, the function $f(x)=|x|$ has two different tangents (left $k=-1$, right $k=1$). Uniqueness is violated, thus the derivative does not exist.",
        "case_1_text": "The function has a derivative, but the remainder does not decrease fast enough.",
        "case_2_text": "The function oscillates too quickly, so the remainder does not stabilize.",
        "conclusion": "In this case, Kapanadze's criterion clearly indicates that the derivative (unique tangent) does not exist.",
        "left_tan": "Left Tangent",
        "right_tan": "Right Tangent"
    }
}

# ==========================================
# ენის არჩევა
# ==========================================
st.sidebar.markdown("### 🌐 Language / ენა")
lang_choice = st.sidebar.radio("", ["ქართული", "English"], horizontal=True)
lang = "KA" if lang_choice == "ქართული" else "EN"
txt = translations[lang]

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

st.sidebar.title(txt["sidebar_title"])
tab_selection = st.sidebar.radio("", txt["nav_options"])

st.title(txt["title"])

# --- მთავარი შეტყობინება ამოღებულია ---

st.markdown("---")

# -----------------------------------------------------------------------------
# TAB 1: გეომეტრია
# -----------------------------------------------------------------------------
if tab_selection == txt["nav_options"][0]:
    st.header(txt["t1_header"])
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<div class='academic-box'>{txt['t1_info']}</div>", unsafe_allow_html=True)
        func_input = st.text_input(f"{txt['func_label']}:", "x^2", key="geom_func")
        x_a = st.number_input(f"{txt['point_a']}:", value=1.0, step=0.1)
        h = st.slider(f"{txt['point_b_dist']}:", 0.01, 2.0, 1.0, 0.01)
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
    
    st.markdown(f"""
    <div class='academic-box'>
        <h4>{txt['t2_thm_title']}</h4>
        <p>{txt['t2_thm_text']}</p>
        <p><i>{txt['t2_thm_sub']}</i></p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        f_in = st.text_input(f"{txt['func_label']}:", "sin(x) * exp(0.5*x)", key="alg_func")
        x0_in = st.number_input(f"{txt['touch_point']}:", value=1.0, step=0.1)
        calc_btn = st.button(txt["calc_btn"], type="primary")
        
    if calc_btn:
        with col2:
            func_sym, k_res, tan_sym = algebraic_derivative(f_in, x0_in)
            if func_sym:
                st.markdown(f"**{txt['result']}:** {txt['slope_found']} `k = {float(k_res):.4f}`")
                st.latex(rf"f'(x) = {sp.latex(k_res)}")
                st.latex(rf"\text{{{txt['tan_eq']}}}: y = {sp.latex(tan_sym)}")
                
                x_range = np.linspace(x0_in - 2, x0_in + 2, 600)
                f_lamb, t_lamb = sp.lambdify('x', func_sym, 'numpy'), sp.lambdify('x', tan_sym, 'numpy')
                y_f, y_t = f_lamb(x_range), t_lamb(x_range)
                with np.errstate(divide='ignore', invalid='ignore'): remainder = (y_f - y_t) / (x_range - x0_in)**2
                
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
    st.markdown(f"<div class='academic-box'>{txt['t3_info']}</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        f3_str = st.text_input(f"{txt['surface_label']}:", "x^2 + y^2 - 0.5*x*y")
        x0, y0 = st.number_input("x0:", 0.0), st.number_input("y0:", 0.0)
        btn_3d = st.button(txt["build_3d"], type="primary")
    if btn_3d:
        with col2:
            func_sym, kx, ky, z0 = solve_kapanadze_3d(f3_str, x0, y0)
            if func_sym:
                st.latex(rf"k_x = {float(kx):.4f}, \quad k_y = {float(ky):.4f}")
                
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
    st.markdown(f"<div class='academic-box'>{txt['t4_info']}</div>", unsafe_allow_html=True)
    
    trig_mode = st.radio(txt["trig_mode_select"], [txt["trig_standard"], txt["trig_inverse"]], horizontal=True)
    
    col1, col2 = st.columns([1, 2])
    
    if trig_mode == txt["trig_standard"]:
        with col1:
            angle = st.slider(f"{txt['angle']}:", 0.0, 2*np.pi, 1.0, 0.1)
            st.markdown(f"**sin(t):** {np.sin(angle):.2f}")
            st.markdown(f"**cos(t):** {np.cos(angle):.2f} ({txt['slope']})")
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
        st.markdown(f"<div class='academic-box'>{txt['inv_info']}</div>", unsafe_allow_html=True)
        with col1:
            val = st.slider(txt["input_val"], -1.0, 1.0, 0.5, 0.01)
            val_tan = val * 5 
            angle_asin = np.arcsin(val)
            angle_acos = np.arccos(val)
            angle_atan = np.arctan(val_tan)
            st.markdown(f"**{txt['inv_res']}:**")
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

# -----------------------------------------------------------------------------
# TAB 5: მაჩვენებლიანი და ლოგარითმული
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][4]:
    st.header(txt["t5_header"])
    st.markdown(f"<div class='academic-box'>{txt['t5_intro']}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    fig = None 
    
    with col1:
        func_mode = st.radio(txt["t5_select_mode"], ["Exponential (e^x)", "Logarithmic (log)"], horizontal=True)
        
        if "Exponential" in func_mode:
            st.markdown(f"<div class='academic-box'>{txt['t5_exp_info']}</div>", unsafe_allow_html=True)
            x0_exp = st.number_input(f"{txt['touch_point']}:", value=1.0, step=0.1)
            val = np.exp(x0_exp)
            slope = val
            st.latex(rf"f(x_0) = e^{{{x0_exp}}} \approx {val:.4f}")
            st.latex(rf"f'(x_0) = e^{{{x0_exp}}} \approx {slope:.4f}")
            st.caption(txt['value_eq_slope'])
            
            x_range = np.linspace(x0_exp - 2, x0_exp + 2, 100)
            y_exp = np.exp(x_range)
            y_tan = val + slope * (x_range - x0_exp)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_range, y=y_exp, name="e^x", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=x_range, y=y_tan, name=txt["tangent"], line=dict(color='red', dash='dash')))
            fig.add_trace(go.Scatter(x=[x0_exp], y=[val], mode='markers+text', text=["P"], textposition="top left", marker=dict(size=12, color='black')))
            fig.update_layout(title="y = e^x", height=500, template="plotly_white")
            
        else:
            st.markdown(f"<div class='academic-box'>{txt['t5_log_info']}</div>", unsafe_allow_html=True)
            base_type = st.selectbox(f"{txt['base_select']}:", txt["bases"])
            x0_log = st.number_input(f"{txt['touch_point']} (x > 0):", value=1.0, step=0.1, min_value=0.01)
            
            if "e" in base_type:
                log_func_str, display_str = "log(x)", "ln(x)"
            elif "10" in base_type:
                log_func_str, display_str = "log(x, 10)", "log_{10}(x)"
            else:
                log_func_str, display_str = "log(x, 2)", "log_{2}(x)"
            
            if st.button(txt["calc_log"], type="primary"):
                func_sym, k_res, tan_sym = algebraic_derivative(log_func_str, x0_log)
                if func_sym:
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
                else:
                    st.error("Error")
        
    with col2:
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 6: კავშირი ნიუტონთან და კოშისთან (დავითის ნახაზის ზუსტი ასლი + ფიზიკა)
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][5]:
    st.header(txt["t6_header"])
    st.markdown(f"<div class='academic-box'>{txt['t6_info']}</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        f_str = "x^2" 
        x0 = st.number_input("x0:", value=1.0, step=0.1)
        dx = st.slider(txt["delta_x_label"], 0.01, 2.0, 1.0, 0.01)
        x = sp.symbols('x')
        f = sp.sympify(f_str)
        f_lamb = sp.lambdify(x, f, 'numpy')
        y0 = f_lamb(x0)
        y_next = f_lamb(x0 + dx)
        delta_F = y_next - y0
        k = float(sp.diff(f, x).subs(x, x0))
        dF = k * dx
        diff_val = delta_F - dF
        
        st.metric(txt["delta_f"] + " (BC)", f"{delta_F:.4f}")
        st.metric(txt["d_f"] + " (BN)", f"{dF:.4f}")
        st.metric(txt["diff_val"] + " (NC)", f"{diff_val:.4f}", delta_color="normal")
        st.info(txt["kapanadze_limit_text"])

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

    # --- ფიზიკის ქვეკატეგორია ---
    st.markdown("---")
    st.header(txt["t8_header"])
    st.markdown(f"<div class='academic-box'>{txt['t8_info']}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        t = st.slider(f"{txt['time']}:", 0.0, 2.0, 0.5, 0.05)
        x_val = t
        y_val = -(t**2) + 2
        vy = -2 * t
        st.markdown(f"**{txt['velocity_vec']}:** (1, {vy:.2f})")
        
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
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 7: განსაკუთრებული შემთხვევები
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][6]:
    st.header(txt["t7_header"])
    st.markdown(f"<div class='academic-box'>{txt['t7_info']}</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        problem_label = st.selectbox(f"{txt['select_case']}:", txt["case_options"])
        if "Absolute" in problem_label or "მოდული" in problem_label:
            st.markdown(txt["case_abs_text"])
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
        st.info(txt["conclusion"])
