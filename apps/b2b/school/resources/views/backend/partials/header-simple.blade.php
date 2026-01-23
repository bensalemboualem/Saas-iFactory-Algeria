<style>
.notification_wrapper .notification_items {
    -webkit-transition: 0.3s;
    transition: 0.3s;
    top: 53px;
    position: absolute;
    z-index: 11;
    -webkit-box-shadow: 0 0 10px 3px rgba(0, 0, 0, 0.05);
    box-shadow: 0 0 10px 3px rgba(0, 0, 0, 0.05);
    width: 300px;
    top: 50px;
    right: 0;
    border-radius: 10px;
    z-index: 121;
    background: #f6f8ff;
    -webkit-transform: translateY(10px) translateX(50%);
    transform: translateY(10px) translateX(50%);
    opacity: 0;
    visibility: hidden;
    transition: 0.3s;
}
</style>

{{-- Header simplifié temporaire pour BBC School Algeria --}}
<div class="navbar-area bg-white" id="stickyadd">
    <div class="navbar">
        <div class="navbar-area-start">
            <span class="sidebar-toggle">
                <i class="fa fa-bars"></i>
            </span>
        </div>
        <div class="navbar-area-end">
            <ul class="nav">
                <li class="nav-item dropdown OT-nav-profile">
                    <a href="#" role="button" id="navbarDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                        <div class="ot-avatar-text">
                            <div class="icon">
                                <i class="fas fa-user"></i>
                            </div>
                            <div>
                                <h6>{{ Auth::user() ? Auth::user()->name : 'Admin' }}</h6>
                                <p>Administrateur BBC School</p>
                            </div>
                        </div>
                    </a>
                    <div class="dropdown-menu dropdown-menu-end ot-card">
                        <div class="card border-0">
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-12 mb-3">
                                        <div class="ot-logout ot-btn-primary">
                                            <form action="{{ route('logout') }}" method="post">
                                                @csrf
                                                <button type="submit" class="btn btn-sm">
                                                    <i class="las la-sign-out-alt"></i>
                                                    {{ ___('common.logout') }}
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</div>