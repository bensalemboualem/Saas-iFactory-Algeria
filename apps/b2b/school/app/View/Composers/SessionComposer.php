<?php

namespace App\View\Composers;

use App\Interfaces\SessionInterface;
use Illuminate\View\View;
use App\Models\Language;

class SessionComposer
{
    /**
     * The user Interface implementation.
     *
     * @var \App\Interfaces\SessionInterface
     */
    protected $session;

    /**
     * Create a new profile composer.
     *
     * @param  \App\Repositories\SessionInterface  $language
     * @return void
     */
    public function __construct(SessionInterface $session)
    {
        $this->session = $session;
    }

    /**
     * Bind data to the view.
     *
     * @param  \Illuminate\View\View  $view
     * @return void
     */
    public function compose(View $view)
    {
        // PERFORMANCE FIX: Cache sessions for 30 minutes
        $session['sessions'] = \Cache::remember('all_sessions', 1800, function () {
            return $this->session->all();
        });

        $currentSessionId = setting('session');
        $session['session'] = \Cache::remember("current_session_{$currentSessionId}", 1800, function () use ($currentSessionId) {
            return $this->session->show($currentSessionId);
        });

        $view->with('session', $session);
    }
}
