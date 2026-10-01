import streamlit as st
import pandas as pd


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Student Attendance Tracker",
    page_icon="📚",
    layout="wide"
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=[
            "Student ID",
            "Student Name",
            "Branch",
            "Year",
            "Section"
        ]
    )

if "attendance" not in st.session_state:
    st.session_state.attendance = pd.DataFrame(
        columns=[
            "Student ID",
            "Student Name",
            "Subject",
            "Total Classes",
            "Classes Attended",
            "Attendance %",
            "Status",
            "Attendance Status"
        ]
    )


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("📚 Student Attendance Tracker")
st.write("A simple application to manage student details and attendance.")


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Add Student",
        "Add Attendance",
        "Attendance Records",
        "Student Records"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================
if page == "Dashboard":

    st.header("📊 Attendance Dashboard")

    students_df = st.session_state.students
    attendance_df = st.session_state.attendance

    # Total students
    total_students = len(students_df)

    # Total classes
    total_classes = pd.to_numeric(
        attendance_df["Total Classes"],
        errors="coerce"
    ).fillna(0).sum()

    # Total attended classes
    total_attended = pd.to_numeric(
        attendance_df["Classes Attended"],
        errors="coerce"
    ).fillna(0).sum()

    # Average attendance
    if len(attendance_df) > 0:
        average_attendance = pd.to_numeric(
            attendance_df["Attendance %"],
            errors="coerce"
        ).fillna(0).mean()
    else:
        average_attendance = 0

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:
        st.metric(
            "📖 Total Classes",
            int(total_classes)
        )

    with col3:
        st.metric(
            "✅ Classes Attended",
            int(total_attended)
        )

    with col4:
        st.metric(
            "📈 Average Attendance",
            f"{average_attendance:.2f}%"
        )

    st.divider()

    # Students below 75%
    st.subheader("⚠️ Students Below 75% Attendance")

    if len(attendance_df) == 0:

        st.info("No attendance records available.")

    else:

        # Calculate student-wise average attendance
        student_summary = (
            attendance_df
            .groupby(["Student ID", "Student Name"])["Attendance %"]
            .mean()
            .reset_index()
        )

        shortage_students = student_summary[
            student_summary["Attendance %"] < 75
        ].copy()

        if len(shortage_students) == 0:

            st.success("🎉 No students have attendance below 75%.")

        else:

            shortage_students["Attendance %"] = (
                shortage_students["Attendance %"].round(2)
            )

            st.dataframe(
                shortage_students,
                use_container_width=True,
                hide_index=True
            )


# =========================================================
# ADD STUDENT
# =========================================================
elif page == "Add Student":

    st.header("👨‍🎓 Student Details")

    with st.form("student_form"):

        student_name = st.text_input(
            "Student Name *",
            placeholder="Enter student name"
        )

        student_id = st.text_input(
            "Student ID / Roll Number *",
            placeholder="Enter student ID"
        )

        branch = st.selectbox(
            "Branch / Department *",
            [
                "CSE",
                "ECE",
                "EEE",
                "ME",
                "CE",
                "IT",
                "AIML",
                "DS",
                "Other"
            ]
        )

        year = st.selectbox(
            "Year *",
            [
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year"
            ]
        )

        section = st.selectbox(
            "Section *",
            [
                "A",
                "B",
                "C",
                "D"
            ]
        )

        submit_student = st.form_submit_button(
            "➕ Add Student"
        )

    if submit_student:

        # Validation
        if not student_name.strip():

            st.error("❌ Please enter the student name.")

        elif not student_id.strip():

            st.error("❌ Please enter the Student ID / Roll Number.")

        else:

            students_df = st.session_state.students

            # Check duplicate Student ID
            if student_id in students_df["Student ID"].astype(str).values:

                st.error(
                    "❌ Student ID already exists. Please use a different ID."
                )

            else:

                new_student = pd.DataFrame(
                    [{
                        "Student ID": student_id,
                        "Student Name": student_name.strip(),
                        "Branch": branch,
                        "Year": year,
                        "Section": section
                    }]
                )

                st.session_state.students = pd.concat(
                    [
                        students_df,
                        new_student
                    ],
                    ignore_index=True
                )

                st.success(
                    f"✅ Student '{student_name}' added successfully!"
                )


# =========================================================
# ADD ATTENDANCE
# =========================================================
elif page == "Add Attendance":

    st.header("📝 Add Attendance")

    students_df = st.session_state.students

    if len(students_df) == 0:

        st.warning(
            "⚠️ No students found. Please add a student first."
        )

    else:

        # Create student selection
        student_options = students_df.apply(
            lambda row:
            f"{row['Student ID']} - {row['Student Name']}",
            axis=1
        ).tolist()

        with st.form("attendance_form"):

            selected_student = st.selectbox(
                "Select Student *",
                student_options
            )

            subject = st.selectbox(
                "Select Subject *",
                [
                    "Java",
                    "Data Structures",
                    "DBMS",
                    "Operating Systems",
                    "Computer Networks",
                    "Python",
                    "AI",
                    "Machine Learning",
                    "Mathematics",
                    "Other"
                ]
            )

            total_classes = st.number_input(
                "Total Classes Conducted *",
                min_value=1,
                value=1,
                step=1
            )

            classes_attended = st.number_input(
                "Classes Attended *",
                min_value=0,
                value=0,
                step=1
            )

            attendance_status = st.selectbox(
                "Attendance Status",
                [
                    "Present",
                    "Absent"
                ]
            )

            submit_attendance = st.form_submit_button(
                "💾 Save Attendance"
            )

        if submit_attendance:

            # Validation
            if classes_attended > total_classes:

                st.error(
                    "❌ Classes attended cannot be greater than total classes."
                )

            else:

                # Extract student ID and name
                selected_id = selected_student.split(" - ")[0]

                selected_row = students_df[
                    students_df["Student ID"].astype(str)
                    == selected_id
                ].iloc[0]

                student_name = selected_row["Student Name"]

                # Calculate attendance percentage
                attendance_percentage = (
                    classes_attended / total_classes
                ) * 100

                # Determine eligibility
                if attendance_percentage >= 75:

                    status = "Eligible"

                else:

                    status = "Shortage"

                # Create new attendance record
                new_record = pd.DataFrame(
                    [{
                        "Student ID": selected_id,
                        "Student Name": student_name,
                        "Subject": subject,
                        "Total Classes": int(total_classes),
                        "Classes Attended": int(classes_attended),
                        "Attendance %": round(
                            attendance_percentage,
                            2
                        ),
                        "Status": status,
                        "Attendance Status": attendance_status
                    }]
                )

                st.session_state.attendance = pd.concat(
                    [
                        st.session_state.attendance,
                        new_record
                    ],
                    ignore_index=True
                )

                # Display result
                if attendance_percentage >= 75:

                    st.success(
                        f"✅ Attendance: {attendance_percentage:.2f}% - Eligible"
                    )

                else:

                    st.warning(
                        f"⚠️ Attendance: {attendance_percentage:.2f}% - Shortage"
                    )


# =========================================================
# ATTENDANCE RECORDS
# =========================================================
elif page == "Attendance Records":

    st.header("📋 Attendance Records")

    attendance_df = st.session_state.attendance

    if len(attendance_df) == 0:

        st.info("No attendance records available.")

    else:

        st.dataframe(
            attendance_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # -------------------------------------------------
        # UPDATE RECORD
        # -------------------------------------------------
        st.subheader("✏️ Update Attendance Record")

        record_numbers = list(range(len(attendance_df)))

        selected_record = st.selectbox(
            "Select Record to Update",
            record_numbers,
            format_func=lambda x:
            f"{x + 1}. "
            f"{attendance_df.iloc[x]['Student Name']} - "
            f"{attendance_df.iloc[x]['Subject']}"
        )

        record = attendance_df.iloc[selected_record]

        with st.form("update_form"):

            update_total = st.number_input(
                "Total Classes",
                min_value=1,
                value=int(record["Total Classes"]),
                step=1
            )

            update_attended = st.number_input(
                "Classes Attended",
                min_value=0,
                value=int(record["Classes Attended"]),
                step=1
            )

            update_status = st.selectbox(
                "Attendance Status",
                [
                    "Present",
                    "Absent"
                ],
                index=(
                    0
                    if record["Attendance Status"] == "Present"
                    else 1
                )
            )

            update_button = st.form_submit_button(
                "🔄 Update Record"
            )

        if update_button:

            if update_attended > update_total:

                st.error(
                    "❌ Classes attended cannot be greater than total classes."
                )

            else:

                new_percentage = (
                    update_attended / update_total
                ) * 100

                if new_percentage >= 75:
                    new_status = "Eligible"
                else:
                    new_status = "Shortage"

                st.session_state.attendance.at[
                    selected_record,
                    "Total Classes"
                ] = int(update_total)

                st.session_state.attendance.at[
                    selected_record,
                    "Classes Attended"
                ] = int(update_attended)

                st.session_state.attendance.at[
                    selected_record,
                    "Attendance %"
                ] = round(new_percentage, 2)

                st.session_state.attendance.at[
                    selected_record,
                    "Status"
                ] = new_status

                st.session_state.attendance.at[
                    selected_record,
                    "Attendance Status"
                ] = update_status

                st.success(
                    "✅ Attendance record updated successfully!"
                )

                st.rerun()

        # -------------------------------------------------
        # DELETE RECORD
        # -------------------------------------------------
        st.subheader("🗑️ Delete Attendance Record")

        delete_record = st.selectbox(
            "Select Record to Delete",
            record_numbers,
            format_func=lambda x:
            f"{x + 1}. "
            f"{attendance_df.iloc[x]['Student Name']} - "
            f"{attendance_df.iloc[x]['Subject']}",
            key="delete_record"
        )

        if st.button("🗑️ Delete Selected Record"):

            st.session_state.attendance = (
                st.session_state.attendance
                .drop(delete_record)
                .reset_index(drop=True)
            )

            st.success(
                "✅ Attendance record deleted successfully!"
            )

            st.rerun()


# =========================================================
# STUDENT RECORDS
# =========================================================
elif page == "Student Records":

    st.header("👨‍🎓 Student Records")

    students_df = st.session_state.students

    if len(students_df) == 0:

        st.info("No student records available.")

    else:

        st.dataframe(
            students_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # -------------------------------------------------
        # DELETE STUDENT
        # -------------------------------------------------
        st.subheader("🗑️ Delete Student")

        student_options = students_df.apply(
            lambda row:
            f"{row['Student ID']} - {row['Student Name']}",
            axis=1
        ).tolist()

        selected_student_delete = st.selectbox(
            "Select Student",
            student_options
        )

        if st.button("🗑️ Delete Student"):

            selected_id = selected_student_delete.split(" - ")[0]

            # Delete student
            st.session_state.students = (
                st.session_state.students[
                    st.session_state.students["Student ID"].astype(str)
                    != selected_id
                ]
                .reset_index(drop=True)
            )

            # Also delete attendance records
            st.session_state.attendance = (
                st.session_state.attendance[
                    st.session_state.attendance["Student ID"].astype(str)
                    != selected_id
                ]
                .reset_index(drop=True)
            )

            st.success(
                "✅ Student and related attendance records deleted."
            )

            st.rerun()


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.sidebar.divider()

st.sidebar.info(
    "📚 Student Attendance Tracker\n\n"
    "Built using Python, Streamlit and Pandas."
)