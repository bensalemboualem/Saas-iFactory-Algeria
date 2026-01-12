<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class InstagramController extends Controller
{
    /**
     * Afficher la galerie Instagram BBC School Algeria
     */
    public function gallery(Request $request)
    {
        $category = $request->get('category');
        $featured = $request->get('featured');
        
        $query = DB::table('bbc_instagram_media')
            ->where('is_approved', true)
            ->orderBy('is_featured', 'desc')
            ->orderBy('posted_at', 'desc');
            
        if ($category) {
            $query->where('category', $category);
        }
        
        if ($featured) {
            $query->where('is_featured', true);
        }
        
        $instagramPhotos = $query->get();
        
        return view('components.instagram-gallery', compact('instagramPhotos'));
    }
    
    /**
     * API pour récupérer les photos Instagram
     */
    public function api(Request $request)
    {
        $photos = DB::table('bbc_instagram_media')
            ->where('is_approved', true)
            ->orderBy('is_featured', 'desc')
            ->orderBy('posted_at', 'desc')
            ->limit(12)
            ->get();
            
        return response()->json([
            'success' => true,
            'data' => $photos,
            'instagram_url' => 'https://www.instagram.com/bbcschoolalgeria',
            'reel_url' => 'https://www.instagram.com/reel/C-_GU55OknJ/'
        ]);
    }
    
    /**
     * Récupérer les photos par catégorie
     */
    public function byCategory($category)
    {
        $photos = DB::table('bbc_instagram_media')
            ->where('category', $category)
            ->where('is_approved', true)
            ->orderBy('posted_at', 'desc')
            ->get();
            
        return response()->json([
            'success' => true,
            'category' => $category,
            'data' => $photos
        ]);
    }
}