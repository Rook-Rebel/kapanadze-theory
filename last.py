import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- გვერდის კონფიგურაცია ---
st.set_page_config(
    page_title="Kapanadze Analytical Laboratory",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS დიზაინი ---
st.markdown("""
<style>
    h1 { font-size: 2.2rem !important; font-weight: 700 !important; }
    h2 { font-size: 1.8rem !important; }
    .info-box {
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(255, 193, 7, 0.15);
        border-left: 5px solid #ffc107;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- თარგმანების ლექსიკონი ---
translations = {
    "KA": {
        "sidebar_title": "ნავიგაცია",
        "nav_options": [
            "I. გეომეტრიული არსი",
            "II. ალგებრული კალკულატორი",
            "III. ტოპოლოგია (3D)",
            "IV. ტრიგონომეტრია",
            "V. მაჩვენებლიანი და ლოგარითმული",
            "VI. ფიზიკა (კინემატიკა)",
            "VII. განსაკუთრებული შემთხვევები"
        ],
        "title": "დავით კაპანაძის ალგებრული და გეომეტრიული ანალიზის ლაბორატორია",
        "core_title": "⚠️ რევოლუციური პრინციპი",
        "core_text": "ბატონი დავითის თეორია ითვლის წარმოებულს **ზღვრების ($\lim$) გარეშე!**",
        "core_sub": "ჩვენ ვიყენებთ სუფთა ალგებრულ მეთოდს: ნაშთის კვადრატზე გაყოფას.",
        "bases": ["e (ნატურალური ln)", "10 (ათობითი)", "2 (ორობითი)"],
        # Tab 1
        "t1_header": "თავი I: როგორ იქცევა მკვეთი მხებად?",
        "t1_info": "მხები არის მდგომარეობა, როდესაც ორი წერტილი ($A$ და $B$) ერთიანდება **ორჯერად ფესვად**.",
        "func_label": "ფუნქცია",
        "point_a": "წერტილი A",
        "point_b_dist": "წერტილი B-ს დაშორება (h)",
        "secant": "მკვეთი",
        "tangent": "მხები",
        "viz_title": "ნახაზის ვიზუალიზაცია",
        # Tab 2
        "t2_header": "თავი II: ნაშთის კვადრატზე გაყოფის მეთოდი",
        "t2_thm_title": "კაპანაძის მთავარი თეორემა:",
        "t2_thm_text": "წრფე $y = k(x-x_0) + f(x_0)$ არის მხები **მაშინ და მხოლოდ მაშინ**, თუ სხვაობა ფუნქციასა და წრფეს შორის იყოფა $(x-x_0)^2$-ზე.",
        "t2_thm_sub": "ეს ნიშნავს, რომ ნაშთის გრაფიკი $x_0$-თან ახლოს არ უნდა გარბოდეს უსასრულობაში.",
        "touch_point": "შეხების წერტილი x0",
        "calc_btn": "გამოთვლა და დამტკიცება",
        "result": "შედეგი",
        "slope_found": "ნაპოვნია დახრილობა",
        "tan_eq": "მხების განტოლება",
        "proof_title": "მტკიცებულება: ნაშთი / (x-x0)²",
        "vis_touch": "ვიზუალური შეხება",
        "residue": "ნაშთი",
        "success_msg": "✔ თეორია დამტკიცდა: მწვანე ხაზი უწყვეტია (არ მიდის უსასრულობაში).",
        "error_msg": "შეცდომა",
        # Tab 3
        "t3_header": "თავი III: კაპანაძის თეორია სივრცეში",
        "t3_info": "3D-ში ვეძებთ მხებ სიბრტყეს, რომელთანაც სხვაობა კვადრატული რიგის მცირეა.",
        "surface_label": "ზედაპირი",
        "build_3d": "აგება 3D",
        "found_partials": "ნაპოვნია",
        "surface": "ზედაპირი",
        "tan_plane": "მხები სიბრტყე",
        # Tab 4
        "t4_header": "თავი XII: ტრიგონომეტრიული ფუნქციები",
        "t4_info": "სინუსის 'სიჩქარე' (წარმოებული) არის კოსინუსი. ეს ჩანს ერთეულოვან წრეწირზე მოძრაობისას.",
        "angle": "კუთხე",
        "slope": "დახრილობა",
        "unit_circle": "ერთეულოვანი წრეწირი",
        "trig_mode_select": "აირჩიეთ რეჟიმი",
        "trig_standard": "ჩვეულებრივი (კუთხე -> მნიშვნელობა)",
        "trig_inverse": "შებრუნებული (მნიშვნელობა -> კუთხე)",
        "input_val": "შეიყვანეთ მნიშვნელობა (x)",
        "inv_res": "შედეგები (კუთხეები)",
        # Tab 5
        "t5_header": "📈 მაჩვენებლიანი და ლოგარითმული ფუნქციები",
        "t5_select_mode": "აირჩიეთ ფუნქცია",
        "t5_exp_info": "ფუნქცია $e^x$ უნიკალურია: მისი წარმოებული (სიჩქარე) ტოლია თავისივე მნიშვნელობის. $f'(x) = e^x$.",
        "t5_log_info": "კაპანაძის მეთოდით: $f(x) = \log_a(x) \Rightarrow f'(x) = \\frac{1}{x \\ln(a)}$",
        "value_eq_slope": "ფუნქციის მნიშვნელობა და დახრა ტოლია!",
        "base_select": "აირჩიეთ ფუძე",
        "calc_log": "გამოთვლა (Log)",
        "residue_analysis": "ნაშთის ანალიზი",
        "graph": "გრაფიკი",
        # Tab 6
        "t6_header": "თავი XIII: ფიზიკური ინტერპრეტაცია",
        "t6_info": "კაპანაძის მეთოდით, მხები არის ის წრფე, რომელსაც სხეული გაყვებოდა, მასზე მოქმედი ძალები რომ უცებ გამქრალიყო.",
        "time": "დრო",
        "velocity_vec": "სიჩქარის ვექტორი",
        "trajectory": "ტრაექტორია",
        "body": "სხეული",
        "inertia": "ინერცია",
        "ground": "მიწა",
        "ballistic": "ბალისტიკური მოძრაობა",
        # Tab 7
        "t7_header": "🔬 თეორიის გამოყენების არეალი",
        "t7_info": "აქ განხილულია ფუნქციები, სადაც 'ნაშთის კვადრატზე გაყოფის' მეთოდი სპეციფიკურ შედეგს იძლევა.",
        "select_case": "აირჩიეთ შემთხვევა",
        "case_options": ["|x| (მოდული 0-ში)", "|x|^1.5 (ნაკლები სიგლუვე)", "x^2 * sin(1/x) (ოსცილაცია)"],
        "case_abs_text": "წერტილში $x=0$ ფუნქციას აქვს ორი მხები (მარცხნიდან $-1$, მარჯვნიდან $1$). მხების ერთადერთობა ირღვევა, ამიტომ წარმოებული არ არსებობს.",
        "case_1_text": "ფუნქციას აქვს წარმოებული, მაგრამ ნაშთი არ მცირდება საკმარისად სწრაფად.",
        "case_2_text": "ფუნქცია ირხევა ძალიან სწრაფად, რის გამოც ნაშთი არ სტაბილურდება.",
        "conclusion": "დასკვნა: ამ კონკრეტულ შემთხვევაში მეთოდი პირდაპირ არ გამოიყენება, რადგან ნაშთი არ აკმაყოფილებს კაპანაძის პირობას.",
        "left_tan": "მარცხენა მხები",
        "right_tan": "მარჯვენა მხები"
    },
    "EN": {
        "sidebar_title": "Navigation",
        "nav_options": [
            "I. Geometric Essence",
            "II. Algebraic Calculator",
            "III. Topology (3D)",
            "IV. Trigonometry",
            "V. Exponential & Logarithmic",
            "VI. Physics (Kinematics)",
            "VII. Special Cases"
        ],
        "title": "David Kapanadze's Algebraic and Geometric Analysis Laboratory",
        "core_title": "⚠️ Core Principle",
        "core_text": "David Kapanadze's theory calculates derivatives **without Limits ($\lim$)!**",
        "core_sub": "We use a pure algebraic method: dividing the remainder by the square.",
        "bases": ["e (Natural ln)", "10 (Decimal)", "2 (Binary)"],
        # Tab 1
        "t1_header": "Chapter I: How Secant becomes Tangent?",
        "t1_info": "A tangent is a state where two intersection points ($A$ and $B$) merge into a **double root**.",
        "func_label": "Function",
        "point_a": "Point A",
        "point_b_dist": "Distance to Point B (h)",
        "secant": "Secant",
        "tangent": "Tangent",
        "viz_title": "Visualization",
        # Tab 2
        "t2_header": "Chapter II: Method of Dividing Remainder by Square",
        "t2_thm_title": "Kapanadze's Main Theorem:",
        "t2_thm_text": "The line $y = k(x-x_0) + f(x_0)$ is a tangent **if and only if** the difference between the function and the line is divisible by $(x-x_0)^2$.",
        "t2_thm_sub": "This means the remainder graph near $x_0$ must not fly off to infinity.",
        "touch_point": "Touch Point x0",
        "calc_btn": "Calculate & Prove",
        "result": "Result",
        "slope_found": "Slope found",
        "tan_eq": "Tangent Equation",
        "proof_title": "Proof: Remainder / (x-x0)²",
        "vis_touch": "Visual Touch",
        "residue": "Remainder",
        "success_msg": "✔ Theory Proven: Green line is continuous (finite).",
        "error_msg": "Error",
        # Tab 3
        "t3_header": "Chapter III: Kapanadze's Theory in Space",
        "t3_info": "In 3D, we look for a tangent plane where the difference is of quadratic order smallness.",
        "surface_label": "Surface",
        "build_3d": "Build 3D",
        "found_partials": "Found",
        "surface": "Surface",
        "tan_plane": "Tangent Plane",
        # Tab 4
        "t4_header": "Chapter XII: Trigonometric Functions",
        "t4_info": "The 'velocity' (derivative) of Sine is Cosine. This is visible when moving on a unit circle.",
        "angle": "Angle",
        "slope": "Slope",
        "unit_circle": "Unit Circle",
        "trig_mode_select": "Select Mode",
        "trig_standard": "Standard (Angle -> Value)",
        "trig_inverse": "Inverse (Value -> Angle)",
        "input_val": "Input Value (x)",
        "inv_res": "Results (Angles)",
        # Tab 5
        "t5_header": "📈 Exponential & Logarithmic Functions",
        "t5_select_mode": "Select Function",
        "t5_exp_info": "Function $e^x$ is unique: its derivative (slope) equals its value. $f'(x) = e^x$.",
        "t5_log_info": "By Kapanadze's method: $f(x) = \log_a(x) \Rightarrow f'(x) = \\frac{1}{x \\ln(a)}$",
        "value_eq_slope": "Function Value equals Slope!",
        "base_select": "Select Base",
        "calc_log": "Calculate (Log)",
        "residue_analysis": "Remainder Analysis",
        "graph": "Graph",
        # Tab 6
        "t6_header": "Chapter XIII: Physical Interpretation",
        "t6_info": "According to Kapanadze, the tangent is the line the body would follow if forces acting on it suddenly vanished.",
        "time": "Time",
        "velocity_vec": "Velocity Vector",
        "trajectory": "Trajectory",
        "body": "Body",
        "inertia": "Inertia",
        "ground": "Ground",
        "ballistic": "Ballistic Motion",
        # Tab 7
        "t7_header": "🔬 Scope of Theory",
        "t7_info": "Here we examine functions where the 'remainder division by square' method yields specific results.",
        "select_case": "Select Case",
        "case_options": ["|x| (Absolute Value at 0)", "|x|^1.5 (Less Smoothness)", "x^2 * sin(1/x) (Oscillation)"],
        "case_abs_text": "At $x=0$, the function has two tangents (left $-1$, right $1$). Uniqueness is violated, so derivative doesn't exist.",
        "case_1_text": "The function has a derivative, but the remainder does not decrease fast enough.",
        "case_2_text": "The function oscillates too quickly, so the remainder does not stabilize.",
        "conclusion": "Conclusion: In this specific case, the method is not directly applicable as the remainder does not satisfy Kapanadze's condition.",
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

# --- მთავარი შეტყობინება ---
st.markdown(f"""
<div class="info-box">
    <h3>{txt["core_title"]}</h3>
    <p>{txt["core_text"]}</p>
    <p style="font-size:0.9em; opacity: 0.8;">{txt["core_sub"]}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# TAB 1: გეომეტრია
# -----------------------------------------------------------------------------
if tab_selection == txt["nav_options"][0]:
    st.header(txt["t1_header"])
    col1, col2 = st.columns([1, 2])
    with col1:
        st.info(txt["t1_info"])
        func_input = st.text_input(f"{txt['func_label']} f(x):", "x^2", key="geom_func")
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
            fig.update_layout(title=txt["viz_title"], height=500)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e: st.error(e)

# -----------------------------------------------------------------------------
# TAB 2: ალგებრული კალკულატორი
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][1]:
    st.header(txt["t2_header"])
    
    with st.container(border=True):
        st.markdown(f"**{txt['t2_thm_title']}**")
        st.markdown(txt['t2_thm_text'])
        st.caption(txt['t2_thm_sub'])

    col1, col2 = st.columns([1, 2])
    with col1:
        f_in = st.text_input(f"{txt['func_label']} f(x):", "sin(x) * exp(0.5*x)", key="alg_func")
        x0_in = st.number_input(f"{txt['touch_point']}:", value=1.0, step=0.1)
        calc_btn = st.button(txt["calc_btn"], type="primary")
        
    if calc_btn:
        with col2:
            func_sym, k_res, tan_sym = algebraic_derivative(f_in, x0_in)
            if func_sym:
                with st.container(border=True):
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
                fig.update_layout(height=700)
                st.plotly_chart(fig, use_container_width=True)
                st.success(txt["success_msg"])
            else: st.error(f"{txt['error_msg']}: {tan_sym}")

# -----------------------------------------------------------------------------
# TAB 3: ტოპოლოგია (3D)
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][2]:
    st.header(txt["t3_header"])
    st.info(txt["t3_info"])
    col1, col2 = st.columns([1, 3])
    with col1:
        f3_str = st.text_input(f"{txt['surface_label']} z = f(x,y):", "x^2 + y^2 - 0.5*x*y")
        x0, y0 = st.number_input("x0:", 0.0), st.number_input("y0:", 0.0)
        btn_3d = st.button(txt["build_3d"], type="primary")
    if btn_3d:
        with col2:
            func_sym, kx, ky, z0 = solve_kapanadze_3d(f3_str, x0, y0)
            if func_sym:
                with st.container(border=True):
                    st.latex(rf"k_x = {float(kx):.4f}, \quad k_y = {float(ky):.4f}")
                
                x_v = np.linspace(x0-2, x0+2, 40)
                X, Y = np.meshgrid(x_v, x_v)
                x_sym, y_sym = sp.symbols('x y')
                Z = sp.lambdify((x_sym, y_sym), func_sym, 'numpy')(X, Y)
                Z_plane = float(z0) + float(kx)*(X-x0) + float(ky)*(Y-y0)
                fig = go.Figure()
                fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8, name=txt["surface"]))
                fig.add_trace(go.Surface(z=Z_plane, x=X, y=Y, colorscale=[[0,'red'],[1,'red']], opacity=0.5, showscale=False, name=txt["tan_plane"]))
                fig.add_trace(go.Scatter3d(x=[x0], y=[y0], z=[float(z0)], mode='markers', marker=dict(size=10, color='black')))
                fig.update_layout(height=700)
                st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: ტრიგონომეტრია (წრეწირი გასწორებულია!)
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][3]:
    st.header(txt["t4_header"])
    st.info(txt["t4_info"])
    
    trig_mode = st.radio(txt["trig_mode_select"], [txt["trig_standard"], txt["trig_inverse"]], horizontal=True)
    
    col1, col2 = st.columns([1, 2])
    
    if trig_mode == txt["trig_standard"]:
        with col1:
            angle = st.slider(f"{txt['angle']} (rad):", 0.0, 2*np.pi, 1.0, 0.1)
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
            
            # FIXED: წრეწირის გეომეტრიის გასწორება (width/height და scaleanchor)
            fig.update_layout(height=600, width=800, showlegend=False)
            fig.update_xaxes(range=[-1.5, 1.5], row=1, col=1)
            fig.update_yaxes(scaleanchor="x", scaleratio=1, range=[-1.5, 1.5], row=1, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        with col1:
            val = st.slider(txt["input_val"], -1.0, 1.0, 0.5, 0.01)
            val_tan = val * 5 
            angle_asin = np.arcsin(val)
            angle_acos = np.arccos(val)
            angle_atan = np.arctan(val_tan)
            
            with st.container(border=True):
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
            fig.update_layout(height=800, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 5: მაჩვენებლიანი და ლოგარითმული (Duplicate ID Fixed)
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][4]:
    st.header(txt["t5_header"])
    
    col1, col2 = st.columns([1, 2])
    
    # ლოგიკა: ჯერ ვქმნით fig-ს, შემდეგ ვხატავთ
    fig = None 
    
    with col1:
        func_mode = st.radio(txt["t5_select_mode"], ["Exponential (e^x)", "Logarithmic (log)"], horizontal=True)
        
        if "Exponential" in func_mode:
            st.info(txt["t5_exp_info"])
            x0_exp = st.number_input(f"{txt['touch_point']}:", value=1.0, step=0.1)
            val = np.exp(x0_exp)
            slope = val
            with st.container(border=True):
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
            fig.update_layout(title="y = e^x", height=500)
            
        else:
            st.info(txt["t5_log_info"])
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
                    with st.container(border=True):
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
                    fig.update_layout(title=f"Graph: {display_str}", height=500)
                else:
                    st.error("Error")
        
    with col2:
        # FIXED: მხოლოდ ერთი გამოძახება
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 6: ფიზიკა
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][5]:
    st.header(txt["t6_header"])
    st.info(txt["t6_info"])
    col1, col2 = st.columns([1, 2])
    with col1:
        t = st.slider(f"{txt['time']} (t):", 0.0, 2.0, 0.5, 0.05)
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
        fig.update_layout(title=txt["ballistic"], height=500, yaxis=dict(range=[-2.5, 2.5], scaleanchor="x", scaleratio=1))
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 7: განსაკუთრებული შემთხვევები
# -----------------------------------------------------------------------------
elif tab_selection == txt["nav_options"][6]:
    st.header(txt["t7_header"])
    st.info(txt["t7_info"])
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
            fig.update_layout(title="y = |x| Corner Point", height=500)
            
        elif problem_type == "1.5":
            x_pos = np.linspace(0, 1, 500)
            x_neg = np.linspace(-1, 0, 500)
            y_pos = x_pos**1.5
            y_neg = np.abs(x_neg)**1.5
            x_all = np.concatenate([x_neg, x_pos])
            y_all = np.concatenate([y_neg, y_pos])
            tangent = np.zeros_like(x_all)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_all, y=y_all, name="|x|^1.5", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=x_all, y=tangent, name=txt["tangent"], line=dict(color='red', dash='dash')))
            with np.errstate(divide='ignore', invalid='ignore'):
                remainder = y_all / (x_all**2)
            fig.add_trace(go.Scatter(x=x_all, y=remainder, name=txt["residue"], line=dict(color='purple')))
            fig.update_layout(title="Analysis", height=600, yaxis=dict(range=[0, 5]))
            
        else: # Oscillation
            y = (x**2) * np.sin(1/(x + 1e-9))
            tangent = np.zeros_like(x)
            with np.errstate(divide='ignore', invalid='ignore'):
                remainder = np.sin(1/(x + 1e-9))
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, name="f(x)", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=x, y=remainder, name=txt["residue"], line=dict(color='purple')))
            fig.update_layout(title="Oscillation", height=600, yaxis=dict(range=[-2, 2]))

        st.plotly_chart(fig, use_container_width=True)
        st.info(txt["conclusion"])
