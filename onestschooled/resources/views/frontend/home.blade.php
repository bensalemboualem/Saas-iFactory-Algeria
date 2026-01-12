@extends('frontend.master')
@section('title')
    {{ settingLocale('application_name') }}
@endsection

@section('main')
    <!-- BANNER::START  -->
    <div class="banner_area banner_active owl-carousel">


        {{-- @dd($sections) --}}

        @foreach ($data['sliders'] as $item)
            <!-- SINGLE_CAROUSEL -->
            <div class="banner_item" data-background="{{ @globalAsset(@$item->upload->path, '1920X700.webp') }}">
                <div class="container">
                    <div class="row d-flex align-items-center justify-content-center">
                        <div class="col-lg-12">
                            <div
                                class="banner_text text-center d-flex justify-content-center align-items-center  flex-column">
                                <h3>{{ @$item->defaultTranslate->name }}</span></h3>
                                <p>{{ @$item->defaultTranslate->description }}</p>
                                <div class="d-flex align-items-center gap_24 justify-content-center flex-wrap">
                                    <a href="{{ route('frontend.about') }}"
                                        class="theme_btn min_windth_200">{{ ___('frontend.read_more') }}</a>
                                    <a href="{{ route('frontend.contact') }}"
                                        class="theme_line_btn min_windth_200">{{ ___('frontend.contact_us') }}</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- END_SINGLE_CAROUSEL -->
        @endforeach




    </div>
    <!-- BANNER::END  -->

    <!-- FACILITES_AREA::START  -->
    <div class="facilites_area">
        <div class="container">
            <div class="row">
                @foreach ($data['counters'] as $item)
                    <div class="col-xl-3 col-lg-3 col-md-6 ">
                        <div class="facilites_box d-flex align-items-center mb_30">
                            <div class="facilites_box_icon">
                                <img height="75" src="{{ @globalAsset(@$item->upload->path, '90X60.webp') }}"
                                    alt="Icon">
                            </div>
                            <div class="facilites_box_content">
                                <h4>{{ @$item->defaultTranslate->total_count }}+</h4>
                                <p>{{ @$item->defaultTranslate->name }}</p>
                            </div>
                        </div>
                    </div>
                @endforeach



            </div>
        </div>
    </div>
    <!-- FACILITES_AREA::END  -->


    <!-- STATEMENT_AREA::START  -->
    <div class="statement_area section_padding">
        <div class="container">
            <div class="row">
                <div class="col-xl-7 col-lg-6 col-md-6">
                    <div class="statement_info mb_30">
                        <h3>{{ @$sections['statement']->defaultTranslate->name }}</h3>

                        <ul class="statement_lists">

                            @foreach ( isset($sections['statement']->defaultTranslate->data) && (is_array($sections['statement']->defaultTranslate->data) ) ? $sections['statement']->defaultTranslate->data : [] as $item)
                                {{-- @dd($item) --}}
                                <li>
                                    <div class="statement_title d-flex align-items-center gap_20">
                                        <div class="icon">
                                            <svg width="25" height="26" viewBox="0 0 25 26" fill="none"
                                                xmlns="http://www.w3.org/2000/svg">
                                                <rect x="12.1931" y="0.806641" width="17.2437" height="17.2437"
                                                    transform="rotate(45 12.1931 0.806641)" fill="#FF5170" />
                                                <rect x="14.7651" y="3.37891" width="13.6062" height="13.6062"
                                                    transform="rotate(45 14.7651 3.37891)" fill="#392C7D" />
                                            </svg>
                                        </div>
                                        <h4>{{ $item['title'] }}</h4>
                                    </div>
                                    <p>{{ $item['description'] }}</p>
                                </li>
                            @endforeach


                        </ul>
                        <a href="{{ route('frontend.about') }}" class="theme_btn">{{ ___('frontend.learn_more') }}</a>
                    </div>
                </div>
                <div class="col-xl-5 col-lg-5 col-md-6">
                    <div class="accreditation_wrapper mb_30">
                        <div class="thumb">
                            <img src="{{ @globalAsset(@$sections['statement']->upload->path, '512X512.webp') }}"
                                alt="Image" class="img-fluid">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- STATEMENT_AREA::END  -->

    <!-- SERVICES_AREA::START  -->
    <div class="services_area" data-background="{{ @globalAsset(@$sections['study_at']->upload->path, '1920X700.webp') }}">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-xl-6">
                    <div class="section__title white_text text-center">
                        <h3>{{ @$sections['study_at']->defaultTranslate->name }}</h3>
                        <p>{{ @$sections['study_at']->defaultTranslate->description }}</p>
                    </div>
                </div>
            </div>
            <div class="row">
                @foreach  ( (isset($sections['study_at']->defaultTranslate->data) &&  is_array($sections['study_at']->defaultTranslate->data)) ? $sections['study_at']->defaultTranslate->data : [] as $key => $item)
                    <div class="col-xl-4 col-md-4">
                        <div class="serevice_box mb_30">
                            <div class="icon">
                                @php $org =  (json_decode($sections['study_at'])->data) ?? []; @endphp

                                <img src="{{ @globalAsset(uploadPath(@$org[$key]->icon), '90X60.webp') }}" alt="Icon">
                            </div>
                            <h3>{{ $item['title'] }}</h3>
                            <p>{{ $item['description'] }}</p>
                        </div>
                    </div>
                @endforeach

            </div>
        </div>
    </div>
    <!-- SERVICES_AREA::END  -->

    <!-- EXPLORER_AREA::START  -->
    <div class="explorer_area section_padding">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-xl-6 col-md-6">
                    <div class="explorer_imgs">
                        <div class="explorer_thumb mb_30">
                            <img src="{{ @globalAsset(@$sections['explore']->upload->path, '512X512.webp') }}"
                                alt="Image" class="img-fluid">
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 col-md-6 mb_25">
                    <div class="section__title mb_30">
                        <h3>{{ @$sections['explore']->defaultTranslate->name }}</h3>
                        <p>{{ @$sections['explore']->defaultTranslate->description }}</p>
                    </div>
                    <div class="nav explorer_tabs" id="nav-tab" role="tablist">

                        @php
                            $exploreData = [];
                            if (isset($sections['explore']->defaultTranslate->data)) {
                                if (is_array($sections['explore']->defaultTranslate->data)) {
                                    $exploreData = $sections['explore']->defaultTranslate->data;
                                } elseif (is_string($sections['explore']->defaultTranslate->data)) {
                                    $exploreData = json_decode($sections['explore']->defaultTranslate->data, true) ?? [];
                                }
                            }
                        @endphp
                        @foreach ($exploreData as $key => $item)
                            <a class="nav-item nav-link {{ $key == 0 ? 'active' : '' }}" id="item{{ $key }}-tab"
                                data-toggle="tab" href="#item{{ $key }}" role="tab"
                                aria-controls="item{{ $key }}" aria-selected="true">{{ $item['tab'] ?? '' }}</a>
                        @endforeach

                    </div>
                    <div class="tab-content explorer_tab_content" id="nav-tabContent">

                        @php
                            $exploreData = [];
                            if (isset($sections['explore']->defaultTranslate->data)) {
                                if (is_array($sections['explore']->defaultTranslate->data)) {
                                    $exploreData = $sections['explore']->defaultTranslate->data;
                                } elseif (is_string($sections['explore']->defaultTranslate->data)) {
                                    $exploreData = json_decode($sections['explore']->defaultTranslate->data, true) ?? [];
                                }
                            }
                        @endphp
                        @foreach ($exploreData as $key => $item)
                            <div class="tab-pane fade {{ $key == 0 ? 'show active' : '' }}" id="item{{ $key }}"
                                role="tabpanel" aria-labelledby="item{{ $key }}-tab">
                                <!-- content ::start  -->
                                <h4 class="explorer_tab_title">{{ $item['title'] ?? '' }}</h4>
                                <p class="explorer_tab_description">{{ $item['description'] ?? '' }}</p>
                                <!-- content ::end  -->
                            </div>
                        @endforeach

                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- EXPLORER_AREA::END  -->

    <!-- TEACHING_AREA::START  -->
    <div class="teaching_area gray_bg section_padding2">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-7 col-md-8">
                    <div class="section__title text-center mb_50">
                        <h3>{{ @$sections['why_choose_us']->defaultTranslate->name }}</h3>
                        <p>{{ @$sections['why_choose_us']->defaultTranslate->description }}</p>
                    </div>
                </div>
            </div>
            <div class="row justify-content-center">
                <div class="col-xl-11">
                    <div class="teaching_grid mb_30">

                        @foreach ( ((isset($sections['why_choose_us']->defaultTranslate->data)) &&  is_array($sections['why_choose_us']->defaultTranslate->data)) ? $sections['why_choose_us']->defaultTranslate->data : [] as $item)
                            <div class="teaching_single d-flex align-items-center">
                                <div class="icon">
                                    <i class="far fa-check-circle"></i>
                                </div>
                                <p>{{ $item }}</p>
                            </div>
                        @endforeach

                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- TEACHING_AREA::END  -->

    <!-- EVENT_AREA::START  -->
    <div class="event_area section_padding">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8 col-md-8">
                    <div class="section__title text-center mb_50">
                        <h3>{{ @$sections['coming_up']->defaultTranslate->name }}</h3>
                        <p>{{ @$sections['coming_up']->defaultTranslate->description }}</p>
                    </div>
                </div>
            </div>
            <div class="row justify-content-center">
                <div class="col-12">

                    <div class="event_wrapper mb_30">
                        <div class="tab-content event_wrapper_content" id="4myTabContent">

                            @foreach ($data['comingEvents'] as $key => $item)
                                <div class="tab-pane fade {{ $key == 0 ? 'show active' : '' }}"
                                    id="event{{ $key }}" role="tabpanel"
                                    aria-labelledby="event{{ $key }}-tab">
                                    <div class="event_wrapper_img">
                                        <img src="{{ @globalAsset(@$item->upload->path, '800X500.webp') }}"
                                            alt="Image" class="img-fluid">
                                    </div>
                                </div>
                            @endforeach

                        </div>
                        <ul class="nav event_tabs" id="4myTab" role="tablist">

                            @foreach ($data['comingEvents'] as $key => $item)
                                <li class="nav-item">
                                    <a class="nav-link {{ $key == 0 ? 'active' : '' }}"
                                        id="event{{ $key }}-tab" data-toggle="tab"
                                        href="#event{{ $key }}" role="tab"
                                        aria-controls="event{{ $key }}"
                                        aria-selected="{{ $key == 0 ? 'true' : 'false' }}">
                                        <div class="icon">
                                            <h3>{{ substr(dateFormat($item->date), 0, 3) }}</h3>
                                            <h5>{{ substr(dateFormat($item->date), 2, 11) }}</h5>
                                        </div>
                                        <div class="event_content">
                                            <span> <i class="far fa-clock"></i>{{ timeFormat($item->start_time) }} -
                                                {{ timeFormat($item->end_time) }}</span>
                                            <p>{{ @$item->defaultTranslate->title }}</p>
                                        </div>
                                    </a>
                                </li>
                            @endforeach

                        </ul>
                    </div>

                </div>
            </div>
        </div>
    </div>
    <!-- EVENT_AREA::END  -->



    <!-- BLOG::START  -->
    <div class="blog_area gray_bg">
        <div class="container-fluid">
            <div class="row justify-content-center">
                <div class="col-lg-6 col-md-8">
                    <div class="section__title text-center mb_80">
                        <h3>{{ @$sections['news']->defaultTranslate->name }}</h3>
                        <p>{{ @$sections['news']->defaultTranslate->description }}</p>
                    </div>
                </div>
            </div>
            <div class="row justify-content-center">
                <div class="blog_grid">
                    <!-- blog_widget  -->
                    @foreach ($data['latestNews'] as $key => $item)
                        @if ($key == 0 || $key == 3)
                            <div class="blog_widget">
                                <a href="{{ route('frontend.news-detail', $item->id) }}" class="thumb">
                                    <img src="{{ @globalAsset(@$item->upload->path, '340X410.webp') }}" alt="Image"
                                        class="w-100">
                                </a>
                                <div class="blog_meta">
                                    <h4>
                                        <a
                                            href="{{ route('frontend.news-detail', $item->id) }}">{{ @$item->defaultTranslate->title }}</a>
                                    </h4>
                                    <p>{!! Str::limit(@$item->defaultTranslate->description, 150) !!}</p>
                                    <div class="blog_bottom d-flex align-items-center justify-content-between">
                                        <a class="blog_readmore d-inline-flex align-items-center gap_10"
                                            href="{{ route('frontend.news-detail', $item->id) }}">
                                            <span class="blog_readmore_text">{{ ___('frontend.read_more') }} </span>
                                            <i class="fas fa-arrow-right"></i>
                                        </a>
                                        <span class="blog_post_date">{{ dateFormat($item->date) }}</span>
                                    </div>
                                </div>
                            </div>
                        @else
                            <div class="blog_widget style2 ">
                                <a href="{{ route('frontend.news-detail', $item->id) }}" class="thumb">
                                    <img src="{{ @globalAsset(@$item->upload->path, '600X480.webp') }}" alt=""
                                        class="w-100">
                                </a>
                                <div class="blog_meta">
                                    <h4>
                                        <a
                                            href="{{ route('frontend.news-detail', $item->id) }}">{{ @$item->defaultTranslate->title }}</a>
                                    </h4>
                                    <p>{!! Str::limit(@$item->defaultTranslate->description, 150) !!}</p>
                                    <div class="blog_bottom d-flex align-items-center justify-content-between">
                                        <a class="blog_readmore d-inline-flex align-items-center gap_10"
                                            href="{{ route('frontend.news-detail', $item->id) }}">
                                            <span class="blog_readmore_text">{{ ___('frontend.read_more') }} </span>
                                            <i class="fas fa-arrow-right"></i>
                                        </a>
                                        <span class="blog_post_date">{{ dateFormat($item->date) }}</span>
                                    </div>
                                </div>
                            </div>
                        @endif
                    @endforeach
                </div>
            </div>
        </div>
    </div>
    <!-- BLOG::END  -->

    <!-- BBC INSTAGRAM GALLERY::START -->
    <div class="instagram_section section_padding3" style="background: #f8f9fa;">
        <div class="container">
            @php
                $instagramPhotos = DB::table('bbc_instagram_media')
                    ->where('is_approved', true)
                    ->orderBy('is_featured', 'desc')
                    ->orderBy('posted_at', 'desc')
                    ->limit(8)
                    ->get();
            @endphp
            
            @if($instagramPhotos->count() > 0)
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <div class="section__title text-center mb_50">
                            <h3>📸 BBC School Algeria sur Instagram</h3>
                            <p>Découvrez la vie de notre école à travers nos photos authentiques</p>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    @foreach($instagramPhotos as $photo)
                    <div class="col-lg-3 col-md-4 col-sm-6 mb_30">
                        <div class="instagram-item" style="position: relative; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); transition: transform 0.3s;">
                            <div class="instagram-thumb" style="position: relative;">
                                <img src="{{ asset($photo->media_url) }}" alt="{{ $photo->caption }}" 
                                     style="width: 100%; height: 250px; object-fit: cover;">
                                <div class="instagram-overlay" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); opacity: 0; transition: opacity 0.3s; display: flex; align-items: center; justify-content: center; flex-direction: column; padding: 20px;">
                                    <div class="instagram-stats" style="color: white; text-align: center;">
                                        <div style="margin-bottom: 15px;">
                                            <i class="fab fa-instagram" style="font-size: 30px; color: #E4405F;"></i>
                                        </div>
                                        <div style="display: flex; gap: 15px; margin-bottom: 15px;">
                                            <span style="font-size: 14px;"><i class="fas fa-heart"></i> {{ $photo->likes_count }}</span>
                                            <span style="font-size: 14px;"><i class="fas fa-comment"></i> {{ $photo->comments_count }}</span>
                                        </div>
                                        <p style="font-size: 12px; margin: 0;">{{ Str::limit($photo->caption, 80) }}</p>
                                    </div>
                                </div>
                            </div>
                            @if($photo->is_featured)
                            <div class="featured-badge" style="position: absolute; top: 10px; right: 10px; background: #E4405F; color: white; padding: 5px 10px; border-radius: 15px; font-size: 10px; font-weight: bold;">
                                ⭐ Featured
                            </div>
                            @endif
                        </div>
                    </div>
                    @endforeach
                </div>
                
                <div class="row">
                    <div class="col-12 text-center mt_30">
                        <a href="https://www.instagram.com/bbcschoolalgeria" target="_blank" 
                           class="theme_btn" style="background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); border: none;">
                            <i class="fab fa-instagram"></i> Suivez-nous @bbcschoolalgeria
                        </a>
                        <a href="https://www.instagram.com/reel/C-_GU55OknJ/" target="_blank" 
                           class="theme_line_btn ml_15">
                            <i class="fas fa-play"></i> Voir le Reel
                        </a>
                    </div>
                </div>
            @endif
        </div>
    </div>
    
    <style>
    .instagram-item:hover {
        transform: translateY(-5px);
    }
    .instagram-item:hover .instagram-overlay {
        opacity: 1;
    }
    .ml_15 {
        margin-left: 15px;
    }
    </style>
    <!-- BBC INSTAGRAM GALLERY::END -->

    <!-- gallery_area::start  -->
    <div class="gallery_area section_padding3">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-7 col-md-8">
                    <div class="section__title text-center mb_30">
                        <h3>{{ @$sections['our_gallery']->defaultTranslate->name }}</h3>
                        <p>{{ @$sections['our_gallery']->defaultTranslate->description }}</p>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <div class="portfolio-menu d-flex gap_24 mb_50 justify-content-center flex-wrap">
                        <button class="active" data-filter="*">{{ ___('frontend.All') }}</button>
                        @foreach ($data['galleryCategory'] as $item)
                            <button data-filter=".{{ $item->id }}">{{ @$item->defaultTranslate->name }}</button>
                        @endforeach
                    </div>
                </div>
            </div>
            <div class="row grid">

                @foreach ($data['gallery'] as $item)
                    <div class="col-lg-3 col-md-4 grid-item {{ $item->gallery_category_id }}">
                        <div class="gallery_box mb_30">
                            <a href="{{ @globalAsset(@$item->upload->path, '340X340.webp') }}"
                                class="thumb overflow-hidden popup-image d-block">
                                <img src="{{ @globalAsset(@$item->upload->path, '340X340.webp') }}" class="img-fluid"
                                    alt="">
                            </a>
                        </div>
                    </div>
                @endforeach

            </div>
        </div>
    </div>
    <!-- gallery_area::end  -->
@endsection
