<?php
/**
 * Menu LiveChat Corrigé - BBC School Algeria
 * Version avec vérifications complètes d'authentification
 */
?>

@if (auth()->check() && auth()->user() && auth()->user()->role_id && 
    (auth()->user()->role_id == \App\Enums\RoleEnum::ADMIN ||
     auth()->user()->role_id == \App\Enums\RoleEnum::SUPERADMIN ||
     auth()->user()->role_id == \App\Enums\RoleEnum::STAFF))

    @if (auth()->user()->role_id == \App\Enums\RoleEnum::SUPERADMIN || auth()->user()->role_id == \App\Enums\RoleEnum::ADMIN)
        @php
            // Vérifier si les routes existent avant de les utiliser
            $liveChatRouteExists = Route::has('admin.live_chat');
            $conversationListExists = Route::has('admin.livechat.conversation_list');
        @endphp
        
        @if($liveChatRouteExists)
        <li class="sidebar-menu-item {{ set_menu(['admin/live-chat*', 'admin/conversation-list*', 'admin/conversation*']) }}">
            <a class="parent-item-content has-arrow" aria-expanded="false">
                <i class="lab la-facebook-messenger"></i>
                <span class="on-half-expanded">{{ ___('settings.Live Chat') }}</span>
            </a>
            <ul class="child-menu-list">
                <li class="sidebar-menu-item {{ set_menu(['admin/live-chat*']) }}">
                    <a href="{{ route('admin.live_chat') }}">
                        {{ ___('settings.Messaging') }}
                    </a>
                </li>
                @if($conversationListExists)
                <li class="sidebar-menu-item {{ set_menu(['admin/conversation-list*', 'admin/conversation*']) }}">
                    <a href="{{ route('admin.livechat.conversation_list') }}">
                        {{ ___('settings.All Conversations') }}
                    </a>
                </li>
                @endif
            </ul>
        </li>
        @endif
    @else
        @php $liveChatRouteExists = Route::has('admin.live_chat'); @endphp
        @if($liveChatRouteExists)
        <li class="sidebar-menu-item {{ set_menu(['admin/live-chat*']) }}">
            <a href="{{ route('admin.live_chat') }}" class="parent-item-content">
                <i class="lab la-facebook-messenger"></i>
                <span class="on-half-expanded">{{ ___('settings.Live Chat') }}</span>
            </a>
        </li>
        @endif
    @endif

@endif

@if (auth()->check() && auth()->user() && auth()->user()->role_id && 
    auth()->user()->role_id == \App\Enums\RoleEnum::TEACHER)
    @php $instructorLiveChatExists = Route::has('instructor.live_chat'); @endphp
    @if($instructorLiveChatExists)
    <li class="sidebar-menu-item {{ set_menu(['instructor/live-chat*']) }}">
        <a href="{{ route('instructor.live_chat') }}" class="parent-item-content">
            <i class="lab la-facebook-messenger"></i>
            <span class="on-half-expanded">{{ ___('settings.Live Chat') }}</span>
        </a>
    </li>
    @endif
@endif

@if (auth()->check() && auth()->user() && auth()->user()->role_id && 
    auth()->user()->role_id == \App\Enums\RoleEnum::STUDENT)
    @php $studentLiveChatExists = Route::has('student.live_chat'); @endphp
    @if($studentLiveChatExists)
    <li class="sidebar-menu-item {{ set_menu(['student/live-chat*']) }}">
        <a href="{{ route('student.live_chat') }}" class="parent-item-content">
            <i class="lab la-facebook-messenger"></i>
            <span class="on-half-expanded">{{ ___('settings.LiveChat') }}</span>
        </a>
    </li>
    @endif
@endif

@if (auth()->check() && auth()->user() && auth()->user()->role_id && 
    auth()->user()->role_id == \App\Enums\RoleEnum::GUARDIAN)
    @php $guardianLiveChatExists = Route::has('guardian.live_chat'); @endphp
    @if($guardianLiveChatExists)
    <li class="sidebar-menu-item {{ set_menu(['guardian/live-chat*']) }}">
        <a href="{{ route('guardian.live_chat') }}" class="parent-item-content">
            <i class="lab la-facebook-messenger"></i>
            <span class="on-half-expanded">{{ ___('settings.Live Chat') }}</span>
        </a>
    </li>
    @endif
@endif
