@extends('frontend.master')
@section('title')
    {{ ___('frontend.contact_us') }}
@endsection

@section('main')


<!-- bradcam::start  -->
<div class="breadcrumb_area" data-background="{{ @globalAsset(@$sections['study_at']->upload->path, '1920X700.webp') }}">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6 col-xl-5">
                <div class="breadcam_wrap text-center">
                    <h3>{{ ___('frontend.contact_us') }}</h3>
                    <div class="custom_breadcam">
                        <a href="{{url('/')}}" class="breadcrumb-item">{{ ___('frontend.home') }}</a>
                        <a href="#" class="breadcrumb-item">{{ ___('frontend.contact_us') }}</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- bradcam::end  -->

<!-- CONTACT::START  -->
<div class="contact_section section_padding2  pb-0">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-7 col-md-8">
                <div class="section__title text-center mb_50">
                    <h3>{!! @$sections['contact_information']->defaultTranslate->name !!}</h3>
                </div>
            </div>
            <div class="col-12">
                <!-- find_content_widget_wrapper  -->
                <div class="find_content_widget_wrapper mb_20">


                    @foreach ($data['contactInfo'] as $item)
                        <div class="find_content_widget d-flex flex-column align-items-center">
                            <div class="icon">
                                <img src="{{ @globalAsset(@$item->upload->path,'65X90.webp') }}" alt="Icon">
                            </div>
                            <h3>{{ @$item->defaultTranslate->name }}</h3>
                            <p>{{ @$item->defaultTranslate->address }}</p>
                        </div>
                    @endforeach


                </div>
            </div>
            <div class="col-12">
                <div class="row justify-content-between">
                    <div class="col-lg-6">
                        <div class="contact_map">
                            <iframe src="https://www.google.com/maps/embed?pb={{setting('map_key')}}" width="100%" height="750" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="contact_form_box mb_30">
                            <div class="section__title mb_50">
                                <h3 class="mb-0 text-white">{{ ___('frontend.leave_a_message') }}</h3>
                            </div>
                            <form class="form-area contact-form" id="myForm" method="post">
                                <div class="row">
                                    <div class="col-xl-6">
                                        <label class="primary_label">{{ ___('frontend.Name') }}</label>
                                        <input name="name" placeholder="{{ ___('frontend.enter_name') }}" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Enter Name'" class="name primary_input mb_30" required="" type="text">
                                    </div>
                                    <div class="col-xl-6">
                                        <label class="primary_label">{{ ___('frontend.phone_no') }}</label>
                                        <input name="phone" placeholder="{{ ___('frontend.phone_no') }}" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Phone no'" class="phone primary_input mb_30" required="" type="text">
                                    </div>
                                    <div class="col-xl-6">
                                        <label class="primary_label">{{ ___('frontend.email_address') }}</label>
                                        <input name="email" placeholder="{{ ___('frontend.type_email_address') }}" pattern="[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{1,63}$" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Type e-mail address'" class="email primary_input mb_30" required="" type="email">

                                    </div>
                                    <div class="col-xl-6">
                                        <label class="primary_label">{{ ___('frontend.Subject') }}</label>
                                        <input name="subject" placeholder="{{ ___('frontend.Subject') }}" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Subject'" class="subject primary_input mb_30" required="" type="text">
                                    </div>
                                    <div class="col-xl-12">
                                        <label class="primary_label">{{ ___('frontend.Message') }}</label>
                                        <textarea class="message primary_textarea mb_30" name="message" placeholder="{{ ___('frontend.write_your_message') }}" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Write your message'" required=""></textarea>
                                    </div>
                                    <div class="col-xl-12 text-left">
                                        <button type="submit" class="theme_btn submit-btn text-center d-inline-flex gap_14 align-items-center m-0">{{ ___('frontend.send_message') }} <i class="fab fa-telegram-plane f_s_20"></i></button>
                                        {{-- mail-script.js --}}
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</div>
<!-- CONTACT::END  -->

<!-- BBC SCHOOL LOCATIONS::START -->
<div class="bbc_locations_area section_padding" style="background: linear-gradient(135deg, #392C7D 0%, #FF5170 100%);">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="section__title mb_50 text-center">
                    <h3 style="color: white;">📍 Nos Établissements BBC School Algeria</h3>
                    <p style="color: rgba(255,255,255,0.9);">Découvrez nos différentes implantations dans la région d'Alger</p>
                </div>
            </div>
        </div>
        <div class="row">
            <!-- Direction Générale - Bouchaoui -->
            <div class="col-lg-4 col-md-6 mb_30">
                <div class="bbc_location_card" style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); height: 100%; transition: transform 0.3s;">
                    <div class="location_icon" style="width: 60px; height: 60px; background: linear-gradient(135deg, #392C7D, #FF5170); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                        <i class="fas fa-building" style="font-size: 24px; color: white;"></i>
                    </div>
                    <h4 style="color: #392C7D; margin-bottom: 15px; font-weight: bold;">🏢 Direction Générale</h4>
                    <div class="location_details">
                        <p style="margin-bottom: 10px;"><i class="fas fa-map-marker-alt" style="color: #FF5170; margin-right: 10px;"></i><strong>Bouchaoui 03, Alger</strong></p>
                        <p style="margin-bottom: 10px;"><i class="fas fa-phone" style="color: #FF5170; margin-right: 10px;"></i><a href="tel:0560089304" style="color: #392C7D;">056 008 93 04</a></p>
                        <p style="margin-bottom: 10px;"><i class="fas fa-phone" style="color: #FF5170; margin-right: 10px;"></i><a href="tel:0540279801" style="color: #392C7D;">054 027 98 01</a></p>
                        <p style="margin-bottom: 0;"><i class="fas fa-envelope" style="color: #FF5170; margin-right: 10px;"></i><a href="mailto:info@bbcschool.net" style="color: #392C7D;">info@bbcschool.net</a></p>
                    </div>
                </div>
            </div>

            <!-- École Principale - Ain Benian -->
            <div class="col-lg-4 col-md-6 mb_30">
                <div class="bbc_location_card" style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); height: 100%; transition: transform 0.3s;">
                    <div class="location_icon" style="width: 60px; height: 60px; background: linear-gradient(135deg, #FF5170, #392C7D); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                        <i class="fas fa-school" style="font-size: 24px; color: white;"></i>
                    </div>
                    <h4 style="color: #392C7D; margin-bottom: 15px; font-weight: bold;">🏫 École Principale</h4>
                    <div class="location_details">
                        <p style="margin-bottom: 10px;"><i class="fas fa-map-marker-alt" style="color: #FF5170; margin-right: 10px;"></i><strong>Route Nationale N°11</strong></p>
                        <p style="margin-bottom: 10px; font-size: 14px; color: #666;">À côté du Barrage fixe de la police</p>
                        <p style="margin-bottom: 10px;"><strong>Ain Benian, Alger</strong></p>
                        <p style="margin-bottom: 10px;"><i class="fas fa-phone" style="color: #FF5170; margin-right: 10px;"></i><a href="tel:0554252325" style="color: #392C7D;">055 425 23 25</a></p>
                        <p style="margin-bottom: 0;"><i class="fas fa-phone" style="color: #FF5170; margin-right: 10px;"></i><a href="tel:0660321772" style="color: #392C7D;">066 032 17 72</a></p>
                    </div>
                </div>
            </div>

            <!-- Annexe - Chéraga -->
            <div class="col-lg-4 col-md-6 mb_30">
                <div class="bbc_location_card" style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); height: 100%; transition: transform 0.3s;">
                    <div class="location_icon" style="width: 60px; height: 60px; background: linear-gradient(135deg, #392C7D, #FF5170); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                        <i class="fas fa-home" style="font-size: 24px; color: white;"></i>
                    </div>
                    <h4 style="color: #392C7D; margin-bottom: 15px; font-weight: bold;">🏠 Annexe Maternelle</h4>
                    <div class="location_details">
                        <p style="margin-bottom: 10px;"><i class="fas fa-map-marker-alt" style="color: #FF5170; margin-right: 10px;"></i><strong>Chéraga, Alger</strong></p>
                        <p style="margin-bottom: 10px;"><i class="fas fa-phone" style="color: #FF5170; margin-right: 10px;"></i><a href="tel:0696012451" style="color: #392C7D;">069 601 24 51</a></p>
                        <p style="margin-bottom: 15px; color: #666; font-size: 14px;">Spécialisé en éducation préscolaire</p>
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-top: 15px;">
                            <p style="margin: 0; font-size: 13px; color: #392C7D;"><i class="fas fa-info-circle" style="margin-right: 5px;"></i>Classes de Maternelle (3-5 ans)</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Horaires et Informations -->
        <div class="row mt_50">
            <div class="col-12">
                <div class="bbc_info_banner" style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 30px; backdrop-filter: blur(10px); border: 2px solid rgba(255,255,255,0.2);">
                    <div class="row align-items-center">
                        <div class="col-lg-6 mb_20">
                            <h4 style="color: white; margin-bottom: 15px;"><i class="far fa-clock" style="margin-right: 10px;"></i>Horaires d'accueil</h4>
                            <p style="color: rgba(255,255,255,0.9); margin-bottom: 5px;"><strong>Dimanche - Jeudi:</strong> 8h00 - 16h00</p>
                            <p style="color: rgba(255,255,255,0.9); margin-bottom: 0;"><strong>Samedi:</strong> 8h00 - 12h00</p>
                        </div>
                        <div class="col-lg-6 mb_20 text-lg-right">
                            <h4 style="color: white; margin-bottom: 15px;"><i class="fas fa-share-alt" style="margin-right: 10px;"></i>Suivez-nous</h4>
                            <div class="social_links">
                                <a href="https://www.facebook.com/bbc.bestbridgeforcreation" target="_blank" style="display: inline-block; width: 40px; height: 40px; background: white; border-radius: 50%; text-align: center; line-height: 40px; margin-right: 10px; transition: transform 0.3s;">
                                    <i class="fab fa-facebook-f" style="color: #392C7D;"></i>
                                </a>
                                <a href="https://www.instagram.com/bbcschoolalgeria" target="_blank" style="display: inline-block; width: 40px; height: 40px; background: white; border-radius: 50%; text-align: center; line-height: 40px; margin-right: 10px; transition: transform 0.3s;">
                                    <i class="fab fa-instagram" style="color: #392C7D;"></i>
                                </a>
                                <a href="https://dz.linkedin.com/company/bbc-school-algeria" target="_blank" style="display: inline-block; width: 40px; height: 40px; background: white; border-radius: 50%; text-align: center; line-height: 40px; transition: transform 0.3s;">
                                    <i class="fab fa-linkedin-in" style="color: #392C7D;"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.bbc_location_card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.3) !important;
}
.social_links a:hover {
    transform: scale(1.1);
}
</style>
<!-- BBC SCHOOL LOCATIONS::END -->

<!-- contact_department_area::start  -->
<div class="contact_department_area section_padding4">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 col-xl-6">
                <div class="section__title mb_76 text-center">
                    <h3 class="text-capitalize">{{ @$sections['department_contact_information']->defaultTranslate->name }}</h3>
                    <p>{{ @$sections['department_contact_information']->defaultTranslate->description }}</p>
                </div>
            </div>
        </div>
        <div class="row">

            @foreach ($data['depContact'] as $item)
                <div class="col-xl-3 col-lg-6 col-md-6">
                    <div class="contact_department_box text-center mb_30">
                        <div class="icon">
                            <img src="{{ @globalAsset(@$item->upload->path, '340X340.webp') }}" alt="Image">
                        </div>
                        <h3>{{ @$item->defaultTranslate->name }}</h3>
                        <p>{{ @$item->defaultTranslate->phone }} <br>
                            {{ @$item->defaultTranslate->email }}</p>
                    </div>
                </div>
            @endforeach

        </div>
    </div>
</div>
<!-- contact_department_area::end  -->

@endsection
