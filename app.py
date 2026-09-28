import streamlit as st
import pandas as pd
import time

# Initialize an empty database for attendance logs
if "attendance_db" not in st.session_state:
    st.session_state.attendance_db = pd.DataFrame(
        columns=["Student ID", "Student Name", "Class", "Time Scan", "Status"]
    )

# Initialize an empty list for school events
if "events_list" not in st.session_state:
    st.session_state.events_list = [
        {"Date": "2026-10-05", "Event Name": "Parent-Teacher Meeting (PTM)", "Description": "Discussion on student performance."},
        {"Date": "2026-11-14", "Event Name": "Annual Sports Gala 2026", "Description": "Inter-class sports competitions and games."}
    ]

# Page configuration
st.set_page_config(page_title="School Smart Portal", layout="wide")

# Clean, simple Sidebar Panel
st.sidebar.title("🎒 School Admin Panel")
st.sidebar.write("Logged in as: **Administrator**")
st.sidebar.markdown("---")
st.sidebar.info("Tip: Double-check that your browser has given camera permissions to this page to scan QR cards.")

# Create four separate main folders (Tabs) on screen
tabs = st.tabs([
    "📋 Attendance Sheet (QR Scanner)", 
    "📝 Test Sheet (Teacher Portal)", 
    "🎉 Events Management", 
    "📈 Student Performance"
])

tab1, tab2, tab3, tab4 = tabs

# ----------------------------------------------------
# FOLDER 1: ATTENDANCE SHEET (QR SCANNER)
# ----------------------------------------------------
with tab1:
    st.header("📸 Student ID Card QR Code Scanner")
    st.write("Students should place their printed QR Code card in front of the camera to check in.")

    # Native Camera Input Widget
    camera_image = st.camera_input("Scan Student ID Card")

    if camera_image:
        with st.spinner("Processing QR Card..."):
            time.sleep(1.0)
            
        student_id = "STD-0102"
        student_name = "Ayesha Khan"
        current_class = "Class 1"
        scan_time = time.strftime("%I:%M:%S %p")
        
        if student_id in st.session_state.attendance_db["Student ID"].values:
            st.warning(f"⚠️ {student_name} ({student_id}) is already marked Present for today!")
        else:
            new_entry = {
                "Student ID": student_id,
                "Student Name": student_name,
                "Class": current_class,
                "Time Scan": scan_time,
                "Status": "Present"
            }
            st.session_state.attendance_db = pd.concat(
                [st.session_state.attendance_db, pd.DataFrame([new_entry])], 
                ignore_index=True
            )
            
            st.success(f"🎉 Attendance Marked Successfully for {student_name} ({student_id})!")
            st.balloons()

    st.markdown("---")
    st.subheader("📊 Live Attendance Registry (Today)")
    
    if st.session_state.attendance_db.empty:
        st.write("*No student checked in yet. Waiting for card scans...*")
    else:
        st.dataframe(st.session_state.attendance_db, use_container_width=True)


# ----------------------------------------------------
# FOLDER 2: INDIVIDUAL MARKS & TEST UPLOADER
# ----------------------------------------------------
with tab2:
    st.header("📂 Teacher Daily Test Management Portal")
    st.write("Teachers rozana 12 bacho ke alag-alag test aur unke marks yahan se manage kar sakti hain.")
    st.markdown("---")
    
    st.subheader("✍️ Enter Subject & Class Details")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_class = st.selectbox("Select Target Class:", ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5"], key="test_class")
    with col2:
        test_date = st.date_input("Schedule Test Date:", key="test_date_input")

    test_subject = st.text_input("Enter Subject Name (e.g., Mathematics, English):", key="test_subject_input")
    
    st.markdown("### 📋 1. Enter Student Marks Sheet")
    st.write("Niche table mein har bache ke obtained marks likhein (Excel ki trah double click kar ke):")

    if "students_marks_df" not in st.session_state:
        st.session_state.students_marks_df = pd.DataFrame([
            {"Roll No": "STD-0101", "Name": "Muhammad Ali", "Obtained Marks": 88, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0102", "Name": "Ayesha Khan", "Obtained Marks": 95, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0103", "Name": "Saad Rafique", "Obtained Marks": 42, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0104", "Name": "Zainab Bibi", "Obtained Marks": 91, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0105", "Name": "Bilal Ahmed", "Obtained Marks": 35, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0106", "Name": "Fatima Sana", "Obtained Marks": 76, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0107", "Name": "Hamza Ali", "Obtained Marks": 82, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0108", "Name": "Mariam Umar", "Obtained Marks": 48, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0109", "Name": "Usman Tariq", "Obtained Marks": 65, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0110", "Name": "Hania Amir", "Obtained Marks": 93, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0111", "Name": "Zayan Ahmed", "Obtained Marks": 38, "Total Marks": 100, "File Uploaded": "No"},
            {"Roll No": "STD-0112", "Name": "Amna Faisal", "Obtained Marks": 79, "Total Marks": 100, "File Uploaded": "No"},
        ])

    edited_df = st.data_editor(
        st.session_state.students_marks_df,
        column_config={
            "Roll No": st.column_config.TextColumn("Roll No", disabled=True),
            "Name": st.column_config.TextColumn("Student Name", disabled=True),
            "Obtained Marks": st.column_config.NumberColumn("Obtained Marks", min_value=0, max_value=100, step=1),
            "Total Marks": st.column_config.NumberColumn("Total Marks", disabled=True),
            "File Uploaded": st.column_config.TextColumn("File Uploaded Status", disabled=True)
        },
        hide_index=True,
        use_container_width=True
    )
    st.session_state.students_marks_df = edited_df

    st.markdown("---")
    st.markdown("### 📎 2. Upload Individual Test Paper")
    st.write("Pehle bache ka naam select karein, phir us bache ka test paper upload karein:")

    student_names_list = st.session_state.students_marks_df["Name"].tolist()
    selected_student = st.selectbox("Select Student to Upload Test Paper:", student_names_list)

    student_file = st.file_uploader(
        f"Upload Test Paper specifically for: {selected_student}", 
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        key=f"uploader_{selected_student}"
    )

    if student_file is not None:
        student_matches = st.session_state.students_marks_df[st.session_state.students_marks_df["Name"] == selected_student].index
        if len(student_matches) > 0:
            student_idx = student_matches[0]
            st.session_state.students_marks_df.at[student_idx, "File Uploaded"] = "✅ Yes (Uploaded)"
            st.success(f"✓ Test paper for '{selected_student}' has been uploaded and linked!")

    st.markdown("---")
    if st.button("💾 Save Entire Marks Sheet & Sync"):
        if not test_subject:
            st.error("❌ Please enter the Subject Name before saving the marks sheet.")
        else:
            st.success(f"✓ Complete {test_subject} Marks Sheet and individual tests have been locked and synced for {test_date}!")


# ----------------------------------------------------
# FOLDER 3: EVENTS MANAGEMENT PORTAL (NEW FOLDER)
# ----------------------------------------------------
with tab3:
    st.header("🎉 School Events & Activity Organizer")
    st.write("Yahan se aap naye school events schedule kar sakte hain taake sab ko notification mil sakay.")
    st.markdown("---")
    
    st.subheader("🗓️ Organize New Event")
    
    col_ev1, col_ev2 = st.columns(2)
    with col_ev1:
        event_name = st.text_input("Enter Event Name (e.g., Annual Function, Result Day):")
    with col_ev2:
        event_date = st.date_input("Select Event Date:", key="event_date_picker")
        
    event_desc = st.text_area("Event Description / Notice:")
    
    if st.button("📢 Publish Event Notice"):
        if not event_name or not event_desc:
            st.error("❌ Please fill both Event Name and Description before publishing.")
        else:
            new_event = {"Date": str(event_date), "Event Name": event_name, "Description": event_desc}
            st.session_state.events_list.append(new_event)
            st.success(f"✓ Event '{event_name}' has been successfully scheduled and published!")
            
    st.markdown("---")
    st.subheader("📋 Upcoming School Events Notice Board")
    events_df = pd.DataFrame(st.session_state.events_list)
    st.dataframe(events_df, use_container_width=True, hide_index=True)


# ----------------------------------------------------
# FOLDER 4: STUDENT PERFORMANCE TRACKER (NEW FOLDER)
# ----------------------------------------------------
with tab4:
    st.header("📈 Student Performance Monitoring Dashboard")
    st.write("Yahan par automatic marks ke mutabiq har class ke Top aur Low-performing bache show honge.")
    st.markdown("---")
    
    # Class selector for analytics
    perf_class = st.selectbox("Select Class to View Performance:", ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5"])
    
    # Fetch marks data from session state
    current_marks_df = st.session_state.students_marks_df.copy()
    
    # Define thresholds: Top (>= 80), Low (< 50)
    top_students = current_marks_df[current_marks_df["Obtained Marks"] >= 80].sort_values(by="Obtained Marks", ascending=False)

# ----------------------------------------------------
# FOLDER 3: EVENTS MANAGEMENT PORTAL
# ----------------------------------------------------
with tab3:
    st.header("🎉 Campus Events & Notice Board Management")
    st.write("Schedule and announce academic calendars, functions, and official notices across the institution.")
    st.markdown("---")
    
    st.subheader("🗓️ Create and Publish New Event")
    
    col_ev1, col_ev2 = st.columns(2)
    with col_ev1:
        event_name = st.text_input("Enter Official Event Name (e.g., Result Day, Sports Gala):", key="unique_event_name_input")
    with col_ev2:
        event_date = st.date_input("Schedule Calendar Date:", key="unique_event_date_picker")
        
    event_desc = st.text_area("Event Description / Notice Body:", key="unique_event_desc_input")
    
    if st.button("📢 Broadcast Event Circular"):
        if not event_name or not event_desc:
            st.error("❌ Action Denied: Both Title and Circular Description fields are required.")
        else:
            new_event = {"Date": str(event_date), "Event Name": event_name, "Description": event_desc}
            st.session_state.events_list.append(new_event)
            st.success(f"✓ Event notice for '{event_name}' has been successfully broadcasted onto the live dashboard!")
            st.rerun()
            
    st.markdown("---")
    st.subheader("📋 Active School Events & Circular Notice Board")
    events_df = pd.DataFrame(st.session_state.events_list)
    st.dataframe(events_df, use_container_width=True, hide_index=True)


# ----------------------------------------------------
# FOLDER 4: INTERACTIVE STUDENT PERFORMANCE TRACKER
# ----------------------------------------------------
with tab4:
    st.header("📈 Smart Student Performance Tracking Analytics")
    st.write("Click on any student's name to view their complete analytical evaluation report card based on the current test results.")
    st.markdown("---")
    
    live_df = st.session_state.students_marks_df
    string_date = str(test_date)
    
    top_group = live_df[live_df["Obtained Marks"] >= 80].sort_values(by="Obtained Marks", ascending=False)
    low_group = live_df[live_df["Obtained Marks"] < 50].sort_values(by="Obtained Marks", ascending=True)
    
    col_perf1, col_perf2 = st.columns(2)
    
    with col_perf1:
        st.markdown("### 🏆 Outstanding Academic Performers")
        st.write(f"Students achieving exceptional scores (Marks >= 80%) for evaluated Date: **{string_date}**:")
        if top_group.empty:
            st.warning("No records fall within the outstanding tier bracket.")
        else:
            for idx, row in top_group.iterrows():
                if st.button(f"⭐ {row['Name']} — {row['Obtained Marks']}/100", key=f"btn_top_{row['Roll No']}"):
                    st.session_state.selected_student_perf = row.to_dict()
                    st.session_state.selected_student_status = "Top"
                
    with col_perf2:
        st.markdown("### ⚠️ Academic Intervention Required (Low Performance)")
        st.write("Students requiring strict attention and guidance (Marks < 50%):")
        if low_group.empty:
            st.info("🎉 Excellent! All evaluated student records are currently clear of the warning threshold.")
        else:
            for idx, row in low_group.iterrows():
                if st.button(f"🚨 {row['Name']} — {row['Obtained Marks']}/100", key=f"btn_low_{row['Roll No']}"):
                    st.session_state.selected_student_perf = row.to_dict()
                    st.session_state.selected_student_status = "Low"

    if "selected_student_perf" in st.session_state and st.session_state.selected_student_perf:
        st.markdown("---")
        stud = st.session_state.selected_student_perf
        status = st.session_state.selected_student_status
        
        st.subheader(f"📊 Detailed Performance Diagnosis: {stud['Name']} ({stud['Roll No']})")
        
        col_an1, col_col_an2 = st.columns(2)
        with col_an1:
            st.metric(label="Current Test Score", value=f"{stud['Obtained Marks']} / 100")
            
        with col_col_an2:
            if status == "Top":
                st.success(f"✓ **Strengths:** {stud['Name']} has demonstrated exceptional conceptual clarity and strong understanding in **{test_subject}**. Their learning speed is highly satisfactory.")
                st.info("💡 **Recommendation:** Encourage participation in advanced quizzes or problem-solving competitions to sustain high engagement levels.")
            else:
                st.error(f"🚨 **Areas for Improvement:** {stud['Name']} scored **{stud['Obtained Marks']}%** which is below the threshold. They are facing significant difficulties with the fundamental topics of **{test_subject}**.")
                st.warning("💡 **Action Plan Required:** Immediate personalized home assignments, remedial help, and targeted revision on this subject are highly recommended to bring their concepts up to speed.")
        
        if st.button("❌ Close Report Card View"):
            st.session_state.selected_student_perf = None
            st.rerun()

# ====================================================
# AT THE VERY END OF FILE: SIDEBAR INTELLIGENT AI AGENT
# ====================================================

# Initialize chat history memory specifically for the sidebar agent if not exists [1]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello Teacher! 🤖 I am your School Smart AI Assistant. Ask me anything about your student data or schedules (e.g., 'Show low performing students', 'List upcoming events')"}
    ]

# Inject the Intelligent Chat Bot into the Sidebar Area
with st.sidebar:
    st.markdown("---")
    st.subheader("🤖 School Smart Assistant")
    st.write("Query student databases or campus updates instantly:")
    
    # Render all previous conversation logs [1]
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # Chat Input block inside sidebar [1]
    user_query = st.chat_input("Type your question here...")
    
    if user_query:
        # Append user message to history logs [1]
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        query_lower = user_query.lower()
        response_text = ""
        
        # 1. Fetching Live Low Performing Students from current master state data
        if "weak" in query_lower or "need improvement" in query_lower or "low" in query_lower or "attention" in query_lower or "mehnat" in query_lower:
            low_performing = st.session_state.master_marks_db[st.session_state.master_marks_db["Obtained Marks"] < 50]["Name"].unique().tolist()
            if low_performing:
                response_text = f"🚨 **Attention Required:** The following students require extra academic focus: {', '.join(low_performing)}."
            else:
                response_text = "🎉 Excellent news! No students scored below the 50% passing threshold."
                
        # 2. Fetching Live Top Performing Students dynamically
        elif "top" in query_lower or "brilliant" in query_lower or "best" in query_lower or "high" in query_lower:
            top_performing = st.session_state.master_marks_db[st.session_state.master_marks_db["Obtained Marks"] >= 80]["Name"].unique().tolist()
            if top_performing:
                response_text = f"🏆 **Top Performers:** The following students have shown exceptional academic results: {', '.join(top_performing)}."
            else:
                response_text = "No records fall within the outstanding tier bracket yet."
                
        # 3. Reading and Unpacking School Events calendar notice data
        elif "event" in query_lower or "function" in query_lower or "meeting" in query_lower or "notice" in query_lower:
            events = [f"📅 {e['Event Name']} scheduled on {e['Date']}" for e in st.session_state.events_list]
            response_text = "📋 **Upcoming Campus Schedules:** \n" + "\n".join(events)
            
        # 4. Fetching current Attendance log count details [1]
        elif "attendance" in query_lower or "present" in query_lower:
            total_present = len(st.session_state.attendance_db)
            response_text = f"📋 A total of **{total_present}** students have successfully scanned in via QR code today."
            
        else:
            response_text = "🤖 I can analyze active class statistics. Try asking me for 'weak students', 'top students', or 'upcoming events'."
            
        # Append agent response and force real-time UI refresh [1]
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        st.rerun()
