<?php

namespace App\View\Composers;

use App\Interfaces\LanguageInterface;
use Illuminate\View\View;
use App\Models\Language;

class LanguageComposer
{
    /**
     * The user Interface implementation.
     *
     * @var \App\Interfaces\LanguageInterface
     */
    protected $language;

    /**
     * Create a new profile composer.
     *
     * @param  \App\Repositories\LanguageInterface  $language
     * @return void
     */
    public function __construct(LanguageInterface $language)
    {
        $this->language = $language;
    }

    /**
     * Bind data to the view.
     *
     * @param  \Illuminate\View\View  $view
     * @return void
     */
    public function compose(View $view)
    {
        // PERFORMANCE FIX: Cache languages for 1 hour
        $language['languages'] = \Cache::remember('all_languages', 3600, function () {
            return $this->language->all();
        });

        $locale = \Session::get('locale', 'en');
        $language['language'] = \Cache::remember("language_{$locale}", 3600, function () use ($locale) {
            return Language::where('code', $locale)->first();
        });

        $view->with('language', $language);
    }
}
