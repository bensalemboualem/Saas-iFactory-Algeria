<?php

namespace Database\Seeders\WebsiteSetup;

use App\Models\ContactInfoTranslate;
use App\Models\Upload;
use App\Models\WebsiteSetup\ContactInfo;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class ContactInfoSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $images = [
            'frontend/img/contact/contact_1.webp',
            'frontend/img/contact/contact_2.webp',
            'frontend/img/contact/contact_3.webp',
            'frontend/img/contact/contact_4.webp',
        ];

        $uploads = [];
        foreach ($images as $key => $value) {
            $row = new Upload();
            $row->path = $value;
            $row->save();

            $uploads[] = $row->id;
        }

        $info = [
            [
                'image' => $uploads[0],
                'name' => 'Our School',
                'address' => '222, Tower Building, Country Hall, California 777, United States',
            ],
            [
                'image' => $uploads[1],
                'name' => 'Our School',
                'address' => '222, Tower Building, Country Hall, California 777, United States',
            ],
            [
                'image' => $uploads[2],
                'name' => 'Our School',
                'address' => '222, Tower Building, Country Hall, California 777, United States',
            ],
            [
                'image' => $uploads[3],
                'name' => 'Our School',
                'address' => '222, Tower Building, Country Hall, California 777, United States',
            ],
        ];

        $bn_info = [
            [
                'name' => 'আমাদের পাঠশালা',
                'address' => '222, টাওয়ার বিল্ডিং, কান্ট্রি হল, ক্যালিফোর্নিয়া 777, মার্কিন যুক্তরাষ্ট্র',
            ],
            [
                'name' => 'আমাদের পাঠশালা',
                'address' => '222, টাওয়ার বিল্ডিং, কান্ট্রি হল, ক্যালিফোর্নিয়া 777, মার্কিন যুক্তরাষ্ট্র',
            ],
            [
                'name' => 'আমাদের পাঠশালা',
                'address' => '222, টাওয়ার বিল্ডিং, কান্ট্রি হল, ক্যালিফোর্নিয়া 777, মার্কিন যুক্তরাষ্ট্র',
            ],
            [
                'name' => 'আমাদের পাঠশালা',
                'address' => '222, টাওয়ার বিল্ডিং, কান্ট্রি হল, ক্যালিফোর্নিয়া 777, মার্কিন যুক্তরাষ্ট্র',
            ],
        ];

        foreach ($info as $key => $value) {
            $row = new ContactInfo();
            $row->upload_id = $value['image'];
            $row->name = $value['name'];
            $row->address = $value['address'];
            $row->save();
        }

        foreach ($info as $key => $value) {
            $row = new ContactInfoTranslate();
            $row->contact_info_id = $key+1;
            $row->locale = 'en';
            $row->name = $value['name'];
            $row->address = $value['address'];
            $row->save();
        }

        foreach ($bn_info as $key => $value) {
            $row = new ContactInfoTranslate();
            $row->contact_info_id = $key+1;
            $row->locale = 'bn';
            $row->name = $value['name'];
            $row->address = $value['address'];
            $row->save();
        }
    }
}
