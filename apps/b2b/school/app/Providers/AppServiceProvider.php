<?php

namespace App\Providers;

use Illuminate\Http\Request;
use App\Models\WebsiteSetup\Page;
use App\Models\SystemNotification;
use Illuminate\Support\Facades\URL;
use Illuminate\Pagination\Paginator;
use Illuminate\Support\Facades\View;
use App\Models\WebsiteSetup\Subscribe;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\ServiceProvider;
use Illuminate\Cache\RateLimiting\Limit;
use Modules\MultiBranch\Entities\Branch;
use App\Models\WebsiteSetup\PageSections;
use Illuminate\Support\Facades\RateLimiter;
use Stancl\Tenancy\Events\TenancyBootstrapped;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {

        // $this->app['events']->listen(TenancyBootstrapped::class, function ($event) {
        // view()->composer('*', function ($view) {

        //     try {

        //         $subscriber = Subscribe::count();
        //         $sections   = PageSections::with('upload')->get();

        //         $sectionArr = [];
        //         foreach($sections as $section){
        //             $sectionArr[$section->key]   = $section;
        //         }

        //         $view->with([
        //             'sections'   => $sectionArr,
        //             'subscriber' => $subscriber,
        //         ]);
        //     } catch (\Exception $e) {
        //         $view->with([
        //             'sections'   => [],
        //             'subscriber' => 0,
        //         ]);
        //     }
        // });
        // });

    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        RateLimiter::for('web', function (Request $request) {
            return Limit::perMinute(2)->by(optional($request->user())->id ?: $request->ip());
        });


        if (env('APP_SAAS')):

            $this->app['events']->listen(TenancyBootstrapped::class, function ($event) {
                view()->composer('*', function ($view) {

                    try {

                        $subscriber = Subscribe::count();
                        $sections = PageSections::with('upload')->get();

                        $sectionArr = [];
                        foreach ($sections as $section) {
                            $sectionArr[$section->key] = $section;
                        }

                        $view->with([
                            'sections' => $sectionArr,
                            'subscriber' => $subscriber,
                        ]);
                    } catch (\Exception $e) {
                        $view->with([
                            'sections' => [],
                            'subscriber' => 0,
                        ]);
                    }


                });

            });
        else:
            // PERFORMANCE FIX: Only compose for frontend views, not ALL views ('*')
            // Cache the data to avoid DB queries on every view
            view()->composer(['frontend.*', 'layouts.*'], function ($view) {

                try {
                    // Cache subscriber count for 1 hour
                    $subscriber = \Cache::remember('subscriber_count', 3600, function () {
                        return Subscribe::count();
                    });

                    // Cache page sections for 1 hour
                    $sectionArr = \Cache::remember('page_sections', 3600, function () {
                        $sections = PageSections::with('upload')->get();
                        $arr = [];
                        foreach ($sections as $section) {
                            $arr[$section->key] = $section;
                        }
                        return $arr;
                    });

                    $view->with([
                        'sections' => $sectionArr,
                        'subscriber' => $subscriber,
                    ]);
                } catch (\Exception $e) {
                    $view->with([
                        'sections' => [],
                        'subscriber' => 0,
                    ]);
                }
            });




        endif;


        view()->composer(['backend.partials.header', 'parent-panel.partials.header'], function ($view) {

            try {
                $notifications = SystemNotification::myNotification();
                $view->with([
                    'notifications' => $notifications
                ]);
            } catch (\Exception $e) {
                $view->with([
                    'notifications' => []
                ]);
            }
        });

        view()->composer(['frontend.partials.footer-content'], function ($view) {
            try {
                // PERFORMANCE FIX: Cache footer pages for 1 hour
                $footer_pages = \Cache::remember('footer_pages', 3600, function () {
                    return Page::where('menu_show', 'footer')->get(['id', 'name', 'slug']);
                });

                $view->with([
                    'footer_pages' => $footer_pages
                ]);
            } catch (\Exception $e) {
                $view->with([
                    'footer_pages' => []
                ]);
            }
        });

        view()->composer(['frontend.partials.menu'], function ($view) {
            try {
                // PERFORMANCE FIX: Cache header pages for 1 hour
                $header_pages = \Cache::remember('header_pages', 3600, function () {
                    return Page::where('menu_show', 'header')->get(['id', 'name', 'slug']);
                });
                $view->with([
                    'header_pages' => $header_pages
                ]);
            } catch (\Exception $e) {
                $view->with([
                    'header_pages' => []
                ]);
            }
        });


        // PERFORMANCE FIX: Cache module and schema checks
        $hasMultiBranch = \Cache::remember('has_multibranch_module', 3600, function () {
            return hasModule('MultiBranch') && Schema::hasTable('branches');
        });

        if ($hasMultiBranch) {
            view()->composer(['backend.partials.header'], function ($view) {
                $branches = \Cache::remember('branches_list', 3600, function () {
                    return Branch::pluck('name', 'id');
                });
                $view->with(['branches' => $branches]);
            });
        }


        if (env('APP_HTTPS') == true) {
            URL::forceScheme('https');
        }
        Paginator::useBootstrap();
    }


}
