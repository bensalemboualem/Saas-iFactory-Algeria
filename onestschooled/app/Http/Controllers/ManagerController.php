<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ManagerController extends Controller
{
    /**
     * SECURITY: This controller has been disabled.
     *
     * The previous implementation allowed database reset via HTTP request,
     * which is a CRITICAL security vulnerability (CWE-749: Exposed Dangerous Method).
     *
     * Database operations should be performed via:
     *   - CLI: php artisan migrate:fresh --seed
     *   - CI/CD deployment scripts
     *   - Never via HTTP endpoints
     */
    public function index()
    {
        abort(403, 'This endpoint has been disabled for security reasons.');
    }
}
