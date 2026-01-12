<?php
/**
 * CORRECTION PHASE 2 - TERMES SPÉCIFIQUES
 * Corrige tous les termes anglais restants (formulaires, placeholders, etc.)
 */

echo "\n========================================\n";
echo "CORRECTION PHASE 2\n";
echo "========================================\n\n";

$langPath = __DIR__ . '/lang';

// Dictionnaire ARABE - Termes spécifiques et phrases
$arabicSpecific = [
    // Form placeholders and labels
    'Enter Name' => 'أدخل الاسم',
    'enter_name' => 'أدخل الاسم',
    'Select Role' => 'اختر الدور',
    'Select leave type' => 'اختر نوع الإجازة',
    'Select Class' => 'اختر الصف',
    'Select Section' => 'اختر القسم',
    'Select Student' => 'اختر الطالب',
    'Select Status' => 'اختر الحالة',
    'Start Date' => 'تاريخ البدء',
    'End Date' => 'تاريخ الانتهاء',
    'Sl No' => 'الرقم التسلسلي',
    'Sr No' => 'الرقم التسلسلي',
    'SR No' => 'الرقم التسلسلي',
    'sr_no' => 'الرقم التسلسلي',
    'sr_no.' => 'الرقم التسلسلي',
    'Requested by' => 'مقدم من',
    'Requested By' => 'مقدم من',
    'Approved by' => 'موافق عليه من',
    'Approved By' => 'موافق عليه من',
    'Request By' => 'مقدم من',
    'No Attachment' => 'لا يوجد مرفق',
    'Import Fees' => 'استيراد الرسوم',
    'Enter discount title' => 'أدخل عنوان الخصم',
    'Enter Discount Title' => 'أدخل عنوان الخصم',
    'add_new' => 'إضافة جديد',
    'Add New' => 'إضافة جديد',
    'print_now' => 'طباعة الآن',
    'Print Now' => 'طباعة الآن',
    'pdf_download' => 'تحميل PDF',
    'Pdf Download' => 'تحميل PDF',
    'Class (Section)' => 'الصف (القسم)',
    'student_name' => 'اسم الطالب',
    'Student Name' => 'اسم الطالب',
    'Roll' => 'الرقم الدراسي',
    'Admission no' => 'رقم القبول',
    'Admission No' => 'رقم القبول',
    'Approval Action' => 'إجراء الموافقة',
    'Expiry Date' => 'تاريخ الانتهاء',
    'Expire Date' => 'تاريخ الانتهاء',
    'e_mail_address' => 'عنوان البريد الإلكتروني',
    'E Mail Address' => 'عنوان البريد الإلكتروني',
    'date_of_birth' => 'تاريخ الميلاد',
    'Date Of Birth' => 'تاريخ الميلاد',
    'Generate Url' => 'إنشاء رابط',
    'Share Date' => 'تاريخ المشاركة',

    // Login and authentication
    'please_add_new_entity_regarding_this' => 'يرجى إضافة كيان جديد بخصوص هذا',
    'Please Add New Entity Regarding This' => 'يرجى إضافة كيان جديد بخصوص هذا',
    'welcome_back_please_login_to_your_account' => 'مرحباً بعودتك، يرجى تسجيل الدخول إلى حسابك',
    'Welcome Back Please Login To Your Account' => 'مرحباً بعودتك، يرجى تسجيل الدخول إلى حسابك',
    'mobile_or_email' => 'الهاتف المحمول أو البريد الإلكتروني',
    'Mobile Or Email' => 'الهاتف المحمول أو البريد الإلكتروني',
    'enter_mobile_or_email' => 'أدخل الهاتف المحمول أو البريد الإلكتروني',
    'Enter Mobile Or Email' => 'أدخل الهاتف المحمول أو البريد الإلكتروني',
    'login_as_superadmin' => 'تسجيل الدخول كمسؤول عام',
    'Login As Superadmin' => 'تسجيل الدخول كمسؤول عام',
    'login_as_admin' => 'تسجيل الدخول كمسؤول',
    'Login As Admin' => 'تسجيل الدخول كمسؤول',
    'login_as_student' => 'تسجيل الدخول كطالب',
    'Login As Student' => 'تسجيل الدخول كطالب',
    'login_as_parent' => 'تسجيل الدخول كولي أمر',
    'Login As Parent' => 'تسجيل الدخول كولي أمر',
    'login_as_teacher' => 'تسجيل الدخول كمعلم',
    'Login As Teacher' => 'تسجيل الدخول كمعلم',

    // Permissions and messages
    'change permission' => 'تغيير الصلاحية',
    'Change Permission' => 'تغيير الصلاحية',
    'Message / Reason' => 'الرسالة / السبب',
    'Fees list' => 'قائمة الرسوم',
    'Fees List' => 'قائمة الرسوم',
    'Leave Date' => 'تاريخ الإجازة',
    'Present Address' => 'العنوان الحالي',
    'Estimate Time (Minutes)' => 'الوقت المقدر (بالدقائق)',
    'create_language' => 'إنشاء لغة',
    'Create Language' => 'إنشاء لغة',
    'enter_start_date' => 'أدخل تاريخ البدء',
    'Enter Start Date' => 'أدخل تاريخ البدء',
    'enter_end_date' => 'أدخل تاريخ الانتهاء',
    'Enter End Date' => 'أدخل تاريخ الانتهاء',
    'enter_your_email' => 'أدخل بريدك الإلكتروني',
    'Enter Your Email' => 'أدخل بريدك الإلكتروني',
    'Select Manager' => 'اختر المدير',
    'Select One' => 'اختر واحداً',
    'select class' => 'اختر الصف',
    'Health Status' => 'الحالة الصحية',
    'Rank in family' => 'الترتيب في العائلة',
    'Rank In Family' => 'الترتيب في العائلة',
    'Number of brothers/sisters' => 'عدد الإخوة/الأخوات',
    'Number Of Brothers/sisters' => 'عدد الإخوة/الأخوات',
    'Student_Image' => 'صورة الطالب',
    'Student Image' => 'صورة الطالب',
    'Guardian_Image' => 'صورة ولي الأمر',
    'Guardian Image' => 'صورة ولي الأمر',

    // Academic specific
    'Current' => 'الحالي',
    'code' => 'الرمز',
    'Code' => 'الرمز',
    'subject/teacher' => 'المادة/المعلم',
    'Subject/teacher' => 'المادة/المعلم',
    'already_exam_assigned_they_will_also_be_deleted!' => 'تم تعيين الامتحان بالفعل، وسيتم حذفه أيضاً!',
    'Already Exam Assigned They Will Also Be Deleted!' => 'تم تعيين الامتحان بالفعل، وسيتم حذفه أيضاً!',
    'start_time' => 'وقت البدء',
    'Start Time' => 'وقت البدء',
    'end_time' => 'وقت الانتهاء',
    'End Time' => 'وقت الانتهاء',
    'room_no' => 'رقم الغرفة',
    'Room No' => 'رقم الغرفة',
    'day' => 'اليوم',
    'Day' => 'اليوم',
    'enter_start_time' => 'أدخل وقت البدء',
    'Enter Start Time' => 'أدخل وقت البدء',
    'create_class' => 'إنشاء صف',
    'Create Class' => 'إنشاء صف',
    'create_section' => 'إنشاء قسم',
    'Create Section' => 'إنشاء قسم',
    'create_subject' => 'إنشاء مادة',
    'Create Subject' => 'إنشاء مادة',
    'enter_code' => 'أدخل الرمز',
    'Enter Code' => 'أدخل الرمز',
    'subject_and_teacher' => 'المادة والمعلم',
    'Subject And Teacher' => 'المادة والمعلم',
    'select_subject' => 'اختر المادة',
    'Select Subject' => 'اختر المادة',
    'select_teacher' => 'اختر المعلم',
    'Select Teacher' => 'اختر المعلم',
    'you_cannot_edit_this' => 'لا يمكنك تعديل هذا',
    'You Cannot Edit This' => 'لا يمكنك تعديل هذا',

    // Student info specific
    'student_category' => 'فئة الطالب',
    'Student Category' => 'فئة الطالب',
    'select_class' => 'اختر الصف',
    'select_section' => 'اختر القسم',
    'guardian_name' => 'اسم ولي الأمر',
    'Guardian Name' => 'اسم ولي الأمر',
    'guardian_mobile' => 'هاتف ولي الأمر',
    'Guardian Mobile' => 'هاتف ولي الأمر',
    'online_admission_setting' => 'إعدادات القبول عبر الإنترنت',
    'Online Admission Setting' => 'إعدادات القبول عبر الإنترنت',
    'select_fees_group' => 'اختر مجموعة الرسوم',
    'Select Fees Group' => 'اختر مجموعة الرسوم',
    'admission_no' => 'رقم القبول',
    'roll_no' => 'الرقم الدراسي',
    'mobile_number' => 'رقم الهاتف المحمول',
    'Mobile Number' => 'رقم الهاتف المحمول',
    'category_list' => 'قائمة الفئات',
    'Category List' => 'قائمة الفئات',
    'promote_list' => 'قائمة الترقية',
    'Promote List' => 'قائمة الترقية',
    'promote_student' => 'ترقية الطالب',
    'Promote Student' => 'ترقية الطالب',
    'promote_students_in_next_session' => 'ترقية الطلاب في الدورة القادمة',
    'Promote Students In Next Session' => 'ترقية الطلاب في الدورة القادمة',
    'promote_session' => 'دورة الترقية',
    'Promote Session' => 'دورة الترقية',
    'select_session' => 'اختر الدورة',
    'Select Session' => 'اختر الدورة',
    'promote_class' => 'صف الترقية',
    'Promote Class' => 'صف الترقية',
    'promote_section' => 'قسم الترقية',
    'Promote Section' => 'قسم الترقية',
    'disabled_list' => 'قائمة المعطلين',
    'Disabled List' => 'قائمة المعطلين',
    'parent_list' => 'قائمة أولياء الأمور',
    'Parent List' => 'قائمة أولياء الأمور',
    'select_student' => 'اختر الطالب',
    'select subject' => 'اختر المادة',
    'parent_edit' => 'تعديل ولي الأمر',
    'Parent Edit' => 'تعديل ولي الأمر',
    'enter_father_name' => 'أدخل اسم الأب',
    'Enter Father Name' => 'أدخل اسم الأب',
    'father_mobile' => 'هاتف الأب',
    'Father Mobile' => 'هاتف الأب',
    'enter_father_mobile' => 'أدخل هاتف الأب',
    'Enter Father Mobile' => 'أدخل هاتف الأب',
    'father_profession' => 'مهنة الأب',
    'Father Profession' => 'مهنة الأب',
    'enter_father_profession' => 'أدخل مهنة الأب',
    'Enter Father Profession' => 'أدخل مهنة الأب',
    'father_image' => 'صورة الأب',
    'Father Image' => 'صورة الأب',
    'enter_mother_name' => 'أدخل اسم الأم',
    'Enter Mother Name' => 'أدخل اسم الأم',
    'mother_mobile' => 'هاتف الأم',
    'Mother Mobile' => 'هاتف الأم',
    'enter_mother_mobile' => 'أدخل هاتف الأم',
    'Enter Mother Mobile' => 'أدخل هاتف الأم',
    'mother_profession' => 'مهنة الأم',
    'Mother Profession' => 'مهنة الأم',
    'mother_image' => 'صورة الأم',
    'Mother Image' => 'صورة الأم',
    'enter_guardian_name' => 'أدخل اسم ولي الأمر',
    'Enter Guardian Name' => 'أدخل اسم ولي الأمر',
    'enter_guardian_mobile' => 'أدخل هاتف ولي الأمر',
    'Enter Guardian Mobile' => 'أدخل هاتف ولي الأمر',
    'guardian_profession' => 'مهنة ولي الأمر',
    'Guardian Profession' => 'مهنة ولي الأمر',
    'enter_guardian_profession' => 'أدخل مهنة ولي الأمر',
    'Enter Guardian Profession' => 'أدخل مهنة ولي الأمر',
    'guardian_image' => 'صورة ولي الأمر',
    'guardian_email' => 'بريد ولي الأمر الإلكتروني',
    'Guardian Email' => 'بريد ولي الأمر الإلكتروني',
    'enter_guardian_email' => 'أدخل بريد ولي الأمر',
    'Enter Guardian Email' => 'أدخل بريد ولي الأمر',
    'guardian_address' => 'عنوان ولي الأمر',
    'Guardian Address' => 'عنوان ولي الأمر',
    'enter_guardian_address' => 'أدخل عنوان ولي الأمر',
    'Enter Guardian Address' => 'أدخل عنوان ولي الأمر',
    'guardian_relation' => 'صلة ولي الأمر',
    'Guardian Relation' => 'صلة ولي الأمر',
    'enter_guardian_relation' => 'أدخل صلة ولي الأمر',
    'Enter Guardian Relation' => 'أدخل صلة ولي الأمر',
    'Job title or designation' => 'المسمى الوظيفي',
    'Job Title Or Designation' => 'المسمى الوظيفي',
    'Company/Organization name' => 'اسم الشركة/المؤسسة',
    'Company/Organization Name' => 'اسم الشركة/المؤسسة',
    'parent_create' => 'إنشاء ولي أمر',
    'Parent Create' => 'إنشاء ولي أمر',
    'Profile Info' => 'معلومات الملف الشخصي',
    'select_shift' => 'اختر الوردية',
    'Select Shift' => 'اختر الوردية',
    'upload_documents' => 'رفع الوثائق',
    'Upload Documents' => 'رفع الوثائق',
    'student_create' => 'إنشاء طالب',
    'Student Create' => 'إنشاء طالب',
    'enter_admission_no' => 'أدخل رقم القبول',
    'Enter Admission No' => 'أدخل رقم القبول',
    'enter_roll_no' => 'أدخل الرقم الدراسي',
    'Enter Roll No' => 'أدخل الرقم الدراسي',
    'enter_first_name' => 'أدخل الاسم الأول',
    'Enter First Name' => 'أدخل الاسم الأول',
    'enter_last_name' => 'أدخل اسم العائلة',
    'Enter Last Name' => 'أدخل اسم العائلة',
    'enter_mobile' => 'أدخل الهاتف المحمول',
    'Enter Mobile' => 'أدخل الهاتف المحمول',
    'enter_email' => 'أدخل البريد الإلكتروني',
    'Enter Email' => 'أدخل البريد الإلكتروني',
    'select Department' => 'اختر القسم',
    'Select Department' => 'اختر القسم',
    'select_religion' => 'اختر الديانة',
    'Select Religion' => 'اختر الديانة',
    'select_gender' => 'اختر الجنس',
    'Select Gender' => 'اختر الجنس',
    'select_category' => 'اختر الفئة',
    'Select Category' => 'اختر الفئة',
    'blood' => 'فصيلة الدم',
    'Blood' => 'فصيلة الدم',
    'select_blood' => 'اختر فصيلة الدم',
    'Select Blood' => 'اختر فصيلة الدم',
    'admission_date' => 'تاريخ القبول',
    'Admission Date' => 'تاريخ القبول',
    'select_parent' => 'اختر ولي الأمر',
    'Select Parent' => 'اختر ولي الأمر',

    // Attendance
    'Monthly Attendance' => 'الحضور الشهري',
    'attendance_already_collected_you_can_edit_record' => 'تم جمع الحضور بالفعل، يمكنك تعديل السجل',
    'Attendance Already Collected You Can Edit Record' => 'تم جمع الحضور بالفعل، يمكنك تعديل السجل',

    // Leave
    'Add Leave Request' => 'إضافة طلب إجازة',
    'Edit Leave Request' => 'تعديل طلب إجازة',

    // Fees
    'Discount Setup' => 'إعداد الخصم',
    'enter_description' => 'أدخل الوصف',
    'Enter Description' => 'أدخل الوصف',
    'due_date' => 'تاريخ الاستحقاق',
    'Due Date' => 'تاريخ الاستحقاق',
    'fine_type' => 'نوع الغرامة',
    'Fine Type' => 'نوع الغرامة',
    'fine_amount' => 'مبلغ الغرامة',
    'Fine Amount' => 'مبلغ الغرامة',
    'students_list' => 'قائمة الطلاب',
    'Students List' => 'قائمة الطلاب',
    'Fees Discount Setup' => 'إعداد خصم الرسوم',
    'Siblings Discount' => 'خصم الإخوة',
    'Set up sibling-based discounts that scale with each child added' => 'إعداد خصومات الإخوة التي تزيد مع كل طفل',
    'Set Up Sibling-based Discounts That Scale With Each Child Added' => 'إعداد خصومات الإخوة التي تزيد مع كل طفل',
    'Discount Title' => 'عنوان الخصم',
    'Discount Percentage' => 'نسبة الخصم',
    'Early Payment Discount' => 'خصم الدفع المبكر',
    'Set up early payment discounts' => 'إعداد خصومات الدفع المبكر',
    'Set Up Early Payment Discounts' => 'إعداد خصومات الدفع المبكر',
    'fees_details' => 'تفاصيل الرسوم',
    'Fees Details' => 'تفاصيل الرسوم',

    // Examination
    'exam_assign' => 'تعيين الامتحان',
    'Exam Assign' => 'تعيين الامتحان',
    'select idcard' => 'اختر بطاقة الهوية',
    'Select Idcard' => 'اختر بطاقة الهوية',
    'select certificate' => 'اختر الشهادة',
    'Select Certificate' => 'اختر الشهادة',
    'exam_title' => 'عنوان الامتحان',
    'Exam Title' => 'عنوان الامتحان',
    'total_mark' => 'إجمالي العلامات',
    'Total Mark' => 'إجمالي العلامات',
    'select_exam_type' => 'اختر نوع الامتحان',
    'Select Exam Type' => 'اختر نوع الامتحان',
    'exam_type' => 'نوع الامتحان',
    'Exam Type' => 'نوع الامتحان',
    'percent_from' => 'النسبة المئوية من',
    'Percent From' => 'النسبة المئوية من',

    // Report
    'short_view' => 'عرض مختصر',
    'Short View' => 'عرض مختصر',
    'details_view' => 'عرض تفصيلي',
    'Details View' => 'عرض تفصيلي',
    'subject_code' => 'رمز المادة',
    'Subject Code' => 'رمز المادة',
    'subject_name' => 'اسم المادة',
    'Subject Name' => 'اسم المادة',
    'Roll Number' => 'الرقم الدراسي',
    'roll_number' => 'الرقم الدراسي',

    // Staff
    'staff_id' => 'رقم الموظف',
    'Staff Id' => 'رقم الموظف',
    'create_staff' => 'إنشاء موظف',
    'Create Staff' => 'إنشاء موظف',
    'enter_staff_id' => 'أدخل رقم الموظف',
    'Enter Staff Id' => 'أدخل رقم الموظف',
    'select_role' => 'اختر الدور',
    'Select Role' => 'اختر الدور',
    'select_designation' => 'اختر المنصب',
    'Select Designation' => 'اختر المنصب',
    'select_department' => 'اختر القسم',
    'enter_date_of_birth' => 'أدخل تاريخ الميلاد',
    'Enter Date Of Birth' => 'أدخل تاريخ الميلاد',
    'enter_joining_date' => 'أدخل تاريخ الالتحاق',
    'Enter Joining Date' => 'أدخل تاريخ الالتحاق',
    'enter_phone' => 'أدخل الهاتف',
    'Enter Phone' => 'أدخل الهاتف',
    'marital_status' => 'الحالة الزوجية',
    'Marital Status' => 'الحالة الزوجية',
    'current_address' => 'العنوان الحالي',
    'Current Address' => 'العنوان الحالي',
    'enter_current_address' => 'أدخل العنوان الحالي',
    'Enter Current Address' => 'أدخل العنوان الحالي',
    'permanent_address' => 'العنوان الدائم',
    'Permanent Address' => 'العنوان الدائم',
    'enter_permanent_address' => 'أدخل العنوان الدائم',
    'Enter Permanent Address' => 'أدخل العنوان الدائم',
    'enter_basic_salary' => 'أدخل الراتب الأساسي',
    'Enter Basic Salary' => 'أدخل الراتب الأساسي',
    'update_staff' => 'تحديث الموظف',
    'Update Staff' => 'تحديث الموظف',

    // Settings
    'enter_you_address' => 'أدخل عنوانك',
    'Enter You Address' => 'أدخل عنوانك',
    'enter_you_phone' => 'أدخل هاتفك',
    'Enter You Phone' => 'أدخل هاتفك',
    'enter_you_email' => 'أدخل بريدك الإلكتروني',
    'Enter You Email' => 'أدخل بريدك الإلكتروني',
    'school_about' => 'حول المدرسة',
    'School About' => 'حول المدرسة',
    'file_system' => 'نظام الملفات',
    'File System' => 'نظام الملفات',
    'twilio_phone_number' => 'رقم هاتف Twilio',
    'Twilio Phone Number' => 'رقم هاتف Twilio',
    'edit_session' => 'تعديل الدورة',
    'Edit Session' => 'تعديل الدورة',
];

// Fonction pour corriger un fichier JSON
function correctJsonFilePhase2($filePath, $translations) {
    if (!file_exists($filePath)) {
        return 0;
    }

    $content = file_get_contents($filePath);
    $data = json_decode($content, true);

    if ($data === null) {
        return 0;
    }

    $corrections = 0;

    foreach ($data as $key => $value) {
        if (isset($translations[$value])) {
            $data[$key] = $translations[$value];
            $corrections++;
        } elseif (isset($translations[$key])) {
            $data[$key] = $translations[$key];
            $corrections++;
        }
    }

    if ($corrections > 0) {
        $jsonContent = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        file_put_contents($filePath, $jsonContent);
    }

    return $corrections;
}

// Correction ARABE
echo "🇩🇿 CORRECTION ARABE PHASE 2\n";
echo "============================\n\n";

$arPath = $langPath . '/ar';
$totalCorrections = 0;

$files = [
    'common.json',
    'academic.json',
    'student_info.json',
    'attendance.json',
    'leave.json',
    'fees.json',
    'examination.json',
    'report.json',
    'staff.json',
    'settings.json',
];

foreach ($files as $file) {
    $filePath = $arPath . '/' . $file;
    $corrections = correctJsonFilePhase2($filePath, $arabicSpecific);
    if ($corrections > 0) {
        echo "✅ $file: $corrections corrections\n";
        $totalCorrections += $corrections;
    }
}

echo "\n📊 TOTAL ARABE: $totalCorrections corrections\n\n";

echo "✅ CORRECTION PHASE 2 TERMINÉE!\n";
echo "⚠️  Nettoyez les caches:\n";
echo "   \"C:/xampp/php/php.exe\" CLEAR_ALL_CACHES_FINAL.php\n\n";

?>
