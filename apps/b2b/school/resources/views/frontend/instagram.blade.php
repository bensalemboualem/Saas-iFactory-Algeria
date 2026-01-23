@extends('frontend.master')

@section('title', 'BBC School Algeria - Instagram Gallery')

@section('main')
<div class="breadcrumb_area">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <div class="breadcrumb_content d-flex align-items-center justify-content-between">
                    <h3>📸 BBC School Algeria sur Instagram</h3>
                    <nav aria-label="breadcrumb">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="{{ route('frontend.home') }}">{{ ___('frontend.Home') }}</a></li>
                            <li class="breadcrumb-item active" aria-current="page">Instagram</li>
                        </ol>
                    </nav>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="gallery_area section_padding">
    <div class="container">
        <!-- Instagram Header -->
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="section__title text-center mb_50">
                    <h2>📱 BBC School Algeria Instagram</h2>
                    <p>Découvrez la vie quotidienne de notre école à travers nos photos et vidéos authentiques</p>
                    <div class="instagram-follow-section mt_30">
                        <a href="https://www.instagram.com/bbcschoolalgeria" target="_blank" 
                           class="theme_btn instagram-btn">
                            <i class="fab fa-instagram"></i> Suivez @bbcschoolalgeria
                        </a>
                        <a href="https://www.instagram.com/reel/C-_GU55OknJ/" target="_blank" 
                           class="theme_line_btn ml_15">
                            <i class="fas fa-play"></i> Voir notre Reel
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Category Filter -->
        <div class="row">
            <div class="col-12">
                <div class="portfolio-menu d-flex gap_24 mb_50 justify-content-center flex-wrap">
                    <button class="active instagram-filter" data-filter="*">Toutes</button>
                    <button class="instagram-filter" data-filter="campus">Campus</button>
                    <button class="instagram-filter" data-filter="students">Étudiants</button>
                    <button class="instagram-filter" data-filter="classes">Classes</button>
                    <button class="instagram-filter" data-filter="transport">Transport</button>
                    <button class="instagram-filter" data-filter="activities">Activités</button>
                </div>
            </div>
        </div>

        <!-- Instagram Photos Grid -->
        <div class="row grid instagram-grid">
            @php
                $instagramPhotos = DB::table('bbc_instagram_media')
                    ->where('is_approved', true)
                    ->orderBy('is_featured', 'desc')
                    ->orderBy('posted_at', 'desc')
                    ->get();
            @endphp

            @foreach($instagramPhotos as $photo)
            <div class="col-lg-4 col-md-6 grid-item instagram-item-wrapper" data-category="{{ $photo->category }}">
                <div class="instagram-photo-card mb_40">
                    <div class="photo-container">
                        <img src="{{ asset($photo->media_url) }}" alt="{{ $photo->caption }}" class="instagram-image">
                        
                        @if($photo->is_featured)
                        <div class="featured-badge">
                            <i class="fas fa-star"></i> Mis en avant
                        </div>
                        @endif
                        
                        <div class="photo-overlay">
                            <div class="overlay-content">
                                <div class="instagram-stats">
                                    <span><i class="fas fa-heart"></i> {{ $photo->likes_count }}</span>
                                    <span><i class="fas fa-comment"></i> {{ $photo->comments_count }}</span>
                                </div>
                                <div class="instagram-icon">
                                    <i class="fab fa-instagram"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="photo-details">
                        <div class="photo-caption">
                            <p>{{ $photo->caption }}</p>
                        </div>
                        
                        @if($photo->hashtags)
                        <div class="photo-hashtags">
                            @foreach(json_decode($photo->hashtags) as $hashtag)
                                <span class="hashtag">{{ $hashtag }}</span>
                            @endforeach
                        </div>
                        @endif
                        
                        <div class="photo-meta">
                            <span class="category-tag category-{{ $photo->category }}">
                                {{ ucfirst($photo->category) }}
                            </span>
                            <span class="post-date">{{ \Carbon\Carbon::parse($photo->posted_at)->diffForHumans() }}</span>
                        </div>
                    </div>
                </div>
            </div>
            @endforeach
        </div>

        <!-- CTA Section -->
        <div class="row">
            <div class="col-12">
                <div class="instagram-cta-section text-center mt_50">
                    <div class="cta-card">
                        <h4>📱 Restez connectés avec BBC School Algeria</h4>
                        <p>Suivez-nous pour plus de moments authentiques de la vie scolaire</p>
                        <div class="cta-buttons">
                            <a href="https://www.instagram.com/bbcschoolalgeria" target="_blank" class="theme_btn instagram-btn">
                                <i class="fab fa-instagram"></i> Instagram
                            </a>
                            <a href="{{ route('frontend.contact') }}" class="theme_line_btn">
                                <i class="fas fa-envelope"></i> Nous Contacter
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.instagram-btn {
    background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%) !important;
    border: none !important;
}

.instagram-photo-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 25px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.instagram-photo-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}

.photo-container {
    position: relative;
    overflow: hidden;
}

.instagram-image {
    width: 100%;
    height: 300px;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.instagram-photo-card:hover .instagram-image {
    transform: scale(1.05);
}

.featured-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    background: #E4405F;
    color: white;
    padding: 8px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    z-index: 2;
}

.photo-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.75);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.instagram-photo-card:hover .photo-overlay {
    opacity: 1;
}

.overlay-content {
    text-align: center;
    color: white;
}

.instagram-stats {
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-bottom: 15px;
    font-size: 16px;
}

.instagram-icon {
    font-size: 40px;
    color: #E4405F;
}

.photo-details {
    padding: 20px;
}

.photo-caption p {
    margin-bottom: 15px;
    line-height: 1.5;
    color: #333;
}

.photo-hashtags {
    margin-bottom: 15px;
}

.hashtag {
    display: inline-block;
    background: #f0f0f0;
    color: #E4405F;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    margin-right: 8px;
    margin-bottom: 5px;
    font-weight: 500;
}

.photo-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
}

.category-tag {
    padding: 4px 10px;
    border-radius: 10px;
    font-weight: bold;
    text-transform: uppercase;
}

.category-campus { background: #e3f2fd; color: #1976d2; }
.category-students { background: #f3e5f5; color: #7b1fa2; }
.category-classes { background: #e8f5e8; color: #388e3c; }
.category-transport { background: #fff3e0; color: #f57c00; }
.category-activities { background: #fce4ec; color: #c2185b; }

.post-date {
    color: #666;
}

.instagram-cta-section {
    margin-top: 60px;
}

.cta-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
}

.cta-card h4 {
    color: white;
    margin-bottom: 15px;
}

.cta-buttons {
    margin-top: 25px;
}

.cta-buttons .theme_btn,
.cta-buttons .theme_line_btn {
    margin: 0 10px;
}

.ml_15 {
    margin-left: 15px;
}

/* Filter Animation */
.instagram-filter {
    transition: all 0.3s ease;
}

.instagram-filter.active {
    background: #E4405F !important;
    color: white !important;
}

/* Responsive */
@media (max-width: 768px) {
    .instagram-image {
        height: 250px;
    }
    
    .cta-buttons .theme_btn,
    .cta-buttons .theme_line_btn {
        display: block;
        margin: 10px auto;
        width: 200px;
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Instagram Filter Functionality
    const filterButtons = document.querySelectorAll('.instagram-filter');
    const items = document.querySelectorAll('.instagram-item-wrapper');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            
            items.forEach(item => {
                if (filter === '*' || item.getAttribute('data-category') === filter) {
                    item.style.display = 'block';
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'scale(1)';
                    }, 100);
                } else {
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        item.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
});
</script>
@endsection