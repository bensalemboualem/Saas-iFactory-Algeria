<?php

namespace Modules\MainApp\Database\Seeders;

use App\Models\Setting;
use App\Traits\CommonHelperTrait;
use Carbon\Carbon;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Crypt;

class SettingSeeder extends Seeder
{
    use CommonHelperTrait;

    public function run()
    {
        $schoolName = env('APP_NAME', 'School');
        $domain = env('APP_DOMAIN', 'school.com');
        Setting::create([
            'name'  => 'application_name',
            'value' => $schoolName . 'Management System',
        ]);
        Setting::create([
            'name'  => 'address',
            'value' => 'Resemont Tower, House 148, Road 13/B, Block E Banani Dhaka 1213.',
        ]);
        Setting::create([
            'name'  => 'phone',
            'value' => '+62 8787 8787',
        ]);
        Setting::create([
            'name'  => 'email',
            'value' => 'info@' . $domain,
        ]);
        Setting::create([
            'name'  => 'school_about',
            'value' => 'School Management Software (SMS) is a digital solution designed to simplify and automate administrative, academic, and operational tasks in educational institutions. It serves as a centralized platform to manage activities such as student records, attendance, fee collection, staff management, academic scheduling, and communication with parents.',
        ]);

        Setting::create([
            'name'  => 'footer_text',
            'value' => '© ' . Carbon::now()->year . ' ' . $schoolName . '. All rights reserved.',
        ]);

        Setting::create([
            'name'  => 'file_system',
            'value' => 'local',
        ]);
        Setting::create([
            'name'  => 'aws_access_key_id',
            'value' => 'AKIA3OGN2RWSJOR5UOTK',
        ]);
        Setting::create([
            'name'  => 'aws_secret_key',
            'value' => 'Vz18p5ELHI6BP9K7iZAzduu+sQCD/KkvbAwElmfX',
        ]);
        Setting::create([
            'name'  => 'aws_region',
            'value' => 'ap-southeast-1',
        ]);
        Setting::create([
            'name'  => 'aws_bucket',
            'value' => $schoolName,
        ]);
        Setting::create([
            'name'  => 'aws_endpoint',
            'value' => 'https://s3.ap-southeast-1.amazonaws.com',
        ]);
        Setting::create([
            'name'  => 'recaptcha_sitekey',
            'value' => '6Lfn6nQhAAAAAKYauxvLddLtcqSn1yqn-HRn_CbN',
        ]);
        Setting::create([
            'name'  => 'recaptcha_secret',
            'value' => '6Lfn6nQhAAAAABOzRtEjhZYB49Dd4orv41thfh02',
        ]);
        Setting::create([
            'name'  => 'recaptcha_status',
            'value' => '0',
        ]);
        Setting::create([
            'name'  => 'mail_drive',
            'value' => 'smtp',
        ]);
        Setting::create([
            'name'  => 'mail_host',
            'value' => 'smtp.gmail.com',
        ]);
        Setting::create([
            'name'  => 'mail_address',
            'value' => 'info@' . $domain,
        ]);
        Setting::create([
            'name'  => 'from_name',
            'value' => $schoolName . ' - School Management System',
        ]);
        Setting::create([
            'name'  => 'mail_username',
            'name'  => 'mail_username',
            'value' => 'info@' . $domain,
        ]);

        // pass
        $mail_password = Crypt::encrypt('ya!@a+TIY^&)$&esT');
        Setting::create([
            'name'  => 'mail_password',
            'value' => $mail_password,
        ]);

        Setting::create([
            'name'  => 'mail_port',
            'value' => '587',
        ]);
        Setting::create([
            'name'  => 'encryption',
            'value' => 'tls',
        ]);
        Setting::create([
            'name'  => 'default_langauge',
            'value' => 'en',
        ]);
        Setting::create([
            'name'  => 'light_logo',
            'value' => 'backend/uploads/settings/light.png',
        ]);
        Setting::create([
            'name'  => 'dark_logo',
            'value' => 'backend/uploads/settings/dark.png',
        ]);
        Setting::create([
            'name'  => 'favicon',
            'value' => 'backend/uploads/settings/favicon.png',
        ]);
        Setting::create([
            'name'  => 'session',
            'value' => 1,
        ]);
        Setting::create([
            'name'  => 'currency_code',
            'value' => 'USD',
        ]);
        Setting::create([
            'name'  => 'map_key',
            'value' => '"!1m18!1m12!1m3!1d3650.776241229233!2d90.40412657620105!3d23.790981078642808!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3755c72b14773d9d%3A0x21df6643cbfa879f!2sSookh!5e0!3m2!1sen!2sbd!4v1711600654298!5m2!1sen!2sbd"',
        ]);

    }
}
