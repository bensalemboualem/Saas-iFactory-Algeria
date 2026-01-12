{{-- BBC School Algeria Instagram Gallery --}}
<div class="instagram-gallery">
    <div class="gallery-header">
        <h3>📸 BBC School Algeria sur Instagram</h3>
        <p>Découvrez la vie de notre école à travers nos photos authentiques</p>
        <a href="https://www.instagram.com/bbcschoolalgeria" target="_blank" class="instagram-follow-btn">
            <i class="fab fa-instagram"></i> Suivez-nous @bbcschoolalgeria
        </a>
    </div>
    
    <div class="gallery-grid">
        @foreach($instagramPhotos as $photo)
        <div class="instagram-item {{ $photo->is_featured ? 'featured' : '' }}" data-category="{{ $photo->category }}">
            <div class="photo-container">
                <img src="{{ asset($photo->media_url) }}" alt="{{ $photo->caption }}" loading="lazy">
                <div class="photo-overlay">
                    <div class="photo-stats">
                        <span><i class="fas fa-heart"></i> {{ $photo->likes_count }}</span>
                        <span><i class="fas fa-comment"></i> {{ $photo->comments_count }}</span>
                    </div>
                    <div class="photo-category">{{ ucfirst($photo->category) }}</div>
                </div>
            </div>
            <div class="photo-caption">
                <p>{{ Str::limit($photo->caption, 120) }}</p>
                <div class="photo-hashtags">
                    @if($photo->hashtags)
                        @foreach(json_decode($photo->hashtags) as $hashtag)
                            <span class="hashtag">{{ $hashtag }}</span>
                        @endforeach
                    @endif
                </div>
                <small class="post-date">{{ $photo->posted_at->diffForHumans() }}</small>
            </div>
        </div>
        @endforeach
    </div>
    
    <div class="gallery-footer">
        <a href="https://www.instagram.com/reel/C-_GU55OknJ/" target="_blank" class="view-more-btn">
            Voir plus sur Instagram
        </a>
    </div>
</div>

<style>
.instagram-gallery {
    max-width: 1200px;
    margin: 40px auto;
    padding: 20px;
}

.gallery-header {
    text-align: center;
    margin-bottom: 30px;
}

.gallery-header h3 {
    font-size: 2rem;
    color: #333;
    margin-bottom: 10px;
}

.instagram-follow-btn {
    display: inline-block;
    background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%);
    color: white;
    padding: 12px 24px;
    border-radius: 25px;
    text-decoration: none;
    font-weight: bold;
    margin-top: 15px;
    transition: transform 0.3s;
}

.instagram-follow-btn:hover {
    transform: translateY(-2px);
}

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.instagram-item {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.instagram-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
}

.instagram-item.featured {
    border: 3px solid #e6683c;
    grid-column: span 1;
}

.photo-container {
    position: relative;
    overflow: hidden;
}

.photo-container img {
    width: 100%;
    height: 250px;
    object-fit: cover;
    transition: transform 0.3s;
}

.instagram-item:hover .photo-container img {
    transform: scale(1.05);
}

.photo-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.7);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 15px;
    opacity: 0;
    transition: opacity 0.3s;
}

.instagram-item:hover .photo-overlay {
    opacity: 1;
}

.photo-stats {
    display: flex;
    gap: 15px;
    color: white;
    font-size: 14px;
}

.photo-category {
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 12px;
    align-self: flex-end;
}

.photo-caption {
    padding: 15px;
}

.photo-caption p {
    margin-bottom: 10px;
    line-height: 1.4;
}

.photo-hashtags {
    margin-bottom: 10px;
}

.hashtag {
    display: inline-block;
    background: #f0f0f0;
    color: #e6683c;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    margin-right: 5px;
    margin-bottom: 5px;
}

.post-date {
    color: #666;
    font-size: 12px;
}

.gallery-footer {
    text-align: center;
}

.view-more-btn {
    background: #333;
    color: white;
    padding: 12px 30px;
    border-radius: 25px;
    text-decoration: none;
    transition: background 0.3s;
}

.view-more-btn:hover {
    background: #555;
}

@media (max-width: 768px) {
    .gallery-grid {
        grid-template-columns: 1fr;
    }
    
    .instagram-item.featured {
        grid-column: span 1;
    }
}
</style>