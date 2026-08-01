/**
 * ============================================
 * PROFESSIONAL BLOG JAVASCRIPT v3.0
 * Premium, Performant, Production-Ready
 * ============================================
 * 
 * Table of Contents:
 * 1. DOM Ready - Core Initialization
 * 2. Bootstrap Components (Tooltips, Popovers, Dropdowns, Modals)
 * 3. Navbar & Scroll Effects (Glass Effect, Hide/Show)
 * 4. Back to Top (Smooth Scroll)
 * 5. Smooth Scrolling (Anchor Links)
 * 6. Lazy Loading Images (Intersection Observer)
 * 7. Scroll Reveal Animations (Fade In Up)
 * 8. Reading Progress Bar (Scroll Tracking)
 * 9. Form Enhancements (Validation, Character Counter, Image Preview)
 * 10. Toast Notifications (Premium Alerts)
 * 11. Newsletter Subscription (AJAX with Loading States)
 * 12. Dark Mode Toggle (Local Storage + System Preference)
 * 13. Infinite Scroll (AJAX with Loading States)
 * 14. Like & Bookmark (Optimistic UI Updates)
 * 15. Comment System (Reply, Vote)
 * 16. Search Autocomplete (Debounced, Keyboard Navigation)
 * 17. Post Preview (Modal)
 * 18. Counter Animation (Intersection Observer)
 * 19. Keyboard Accessibility (Shortcuts: ESC, Ctrl+K, Ctrl+Shift+D)
 * 20. Active Nav Highlight (Current Page)
 * 21. Ripple Effect (Buttons)
 * 22. Copy to Clipboard (Fallback Support)
 * 23. Reduced Motion Support (Accessibility)
 * 24. Page Transition (Smooth Load)
 * 25. Utilities & Performance Optimizations
 * ============================================
 */

(function($) {
    'use strict';

    // ============================================
    // 1. DOM READY - Core Initialization
    // ============================================
    $(document).ready(function() {

        // ============================================
        // 2. BOOTSTRAP COMPONENTS INITIALIZATION
        // ============================================
        
        // Tooltips - with custom options
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
                trigger: 'hover focus',
                placement: 'top',
                delay: { show: 100, hide: 100 }
            });
        });

        // Popovers - with custom options
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl, {
                trigger: 'click',
                placement: 'bottom',
                delay: { show: 100, hide: 100 }
            });
        });

        // Dropdowns - with smooth animation
        const dropdownTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="dropdown"]'));
        dropdownTriggerList.map(function(dropdownTriggerEl) {
            return new bootstrap.Dropdown(dropdownTriggerEl, {
                popperConfig: function(defaultBsPopperConfig) {
                    return {
                        ...defaultBsPopperConfig,
                        modifiers: [
                            ...defaultBsPopperConfig.modifiers,
                            {
                                name: 'offset',
                                options: {
                                    offset: [0, 8]
                                }
                            }
                        ]
                    };
                }
            });
        });

        // Modals - with focus management
        const modalTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="modal"]'));
        modalTriggerList.map(function(modalTriggerEl) {
            const target = modalTriggerEl.dataset.bsTarget || modalTriggerEl.getAttribute('href');
            if (target && target.startsWith('#')) {
                const modalEl = document.querySelector(target);
                if (modalEl) {
                    return new bootstrap.Modal(modalEl, {
                        backdrop: true,
                        keyboard: true,
                        focus: true
                    });
                }
            }
        });

        // ============================================
        // 3. NAVBAR & SCROLL EFFECTS (Premium Glass)
        // ============================================
        
        const $navbar = $('.navbar');
        const navbarHeight = $navbar.outerHeight();
        let lastScrollY = 0;
        let ticking = false;

        $(window).on('scroll', function() {
            if (!ticking) {
                window.requestAnimationFrame(function() {
                    const currentScrollY = window.pageYOffset || document.documentElement.scrollTop;
                    
                    // Add shadow when scrolled
                    if (currentScrollY > 50) {
                        $navbar.addClass('scrolled');
                    } else {
                        $navbar.removeClass('scrolled');
                    }

                    // Hide navbar on scroll down, show on scroll up
                    if (currentScrollY > 200 && currentScrollY > lastScrollY) {
                        $navbar.css('transform', 'translateY(-100%)');
                    } else {
                        $navbar.css('transform', 'translateY(0)');
                    }

                    lastScrollY = currentScrollY;
                    ticking = false;
                });
                ticking = true;
            }
        });

        // ============================================
        // 4. BACK TO TOP (Smooth Scroll)
        // ============================================
        
        const $backToTop = $('#back-to-top');
        if ($backToTop.length) {
            $(window).on('scroll', function() {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                if (scrollTop > 300) {
                    $backToTop.fadeIn(300);
                } else {
                    $backToTop.fadeOut(300);
                }
            });

            $backToTop.on('click', function(e) {
                e.preventDefault();
                $('html, body').animate({
                    scrollTop: 0
                }, 600, 'easeInOutCubic');
            });

            $backToTop.attr('aria-label', 'Back to top');
        }

        // ============================================
        // 5. SMOOTH SCROLLING (Anchor Links)
        // ============================================
        
        $('a[href*="#"]:not([href="#"])').on('click', function(e) {
            const href = $(this).attr('href');
            const targetId = href.substring(href.indexOf('#'));
            const $target = $(targetId);
            
            if ($target.length) {
                e.preventDefault();
                const offsetTop = $target.offset().top - (navbarHeight + 20);
                $('html, body').animate({
                    scrollTop: offsetTop
                }, 600, 'easeInOutCubic');
            }
        });

        // ============================================
        // 6. LAZY LOADING IMAGES (Intersection Observer)
        // ============================================
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        const src = img.dataset.src;
                        if (src) {
                            img.src = src;
                            img.removeAttribute('data-src');
                            img.style.opacity = '1';
                            img.classList.add('fade-in');
                        }
                        imageObserver.unobserve(img);
                    }
                });
            }, {
                rootMargin: '100px 0px',
                threshold: 0.01
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }

        // ============================================
        // 7. SCROLL REVEAL ANIMATIONS (Fade In Up)
        // ============================================
        
        if ('IntersectionObserver' in window) {
            const revealObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const el = entry.target;
                        if (!el.classList.contains('revealed')) {
                            el.classList.add('fade-in-up', 'revealed');
                            el.style.opacity = '1';
                        }
                        revealObserver.unobserve(el);
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '20px 0px'
            });

            document.querySelectorAll('.reveal, .post-item, .card, .stat-card, .dashboard-card').forEach(el => {
                el.style.opacity = '0';
                revealObserver.observe(el);
            });
        }

        // ============================================
        // 8. READING PROGRESS BAR
        // ============================================
        
        const $progressBar = $('#reading-progress');
        if ($progressBar.length) {
            let ticking = false;
            $(window).on('scroll', function() {
                if (!ticking) {
                    window.requestAnimationFrame(function() {
                        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                        const docHeight = $(document).height() - $(window).height();
                        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
                        $progressBar.css('width', Math.min(progress, 100) + '%');
                        ticking = false;
                    });
                    ticking = true;
                }
            });
        }

        // ============================================
        // 9. FORM ENHANCEMENTS
        // ============================================
        
        // Bootstrap 5 Form Validation
        const forms = document.querySelectorAll('.needs-validation');
        forms.forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });

        // Character Counter
        $('textarea[maxlength]').each(function() {
            const $textarea = $(this);
            const maxLength = parseInt($textarea.attr('maxlength'));
            const $counter = $('<span class="char-counter text-muted small ms-2"></span>');
            
            const $parent = $textarea.closest('.form-group, .mb-3');
            if ($parent.length) {
                $parent.append($counter);
            } else {
                $textarea.after($counter);
            }

            function updateCounter() {
                const current = $textarea.val().length;
                const remaining = maxLength - current;
                $counter.text(remaining + ' characters remaining');
                if (remaining < 20) {
                    $counter.css('color', '#DC2626');
                } else {
                    $counter.css('color', '#64748B');
                }
            }

            $textarea.on('input', updateCounter);
            updateCounter();
        });

        // Image Upload Preview
        $('input[type="file"]').on('change', function() {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                const $preview = $(this).closest('.form-group, .mb-3').find('.image-preview');
                
                reader.onload = function(e) {
                    $preview.html(
                        '<img src="' + e.target.result + 
                        '" class="img-fluid rounded mt-2" style="max-height:200px;object-fit:cover;border:1px solid #E2E8F0;">'
                    ).show();
                };
                reader.readAsDataURL(file);
            }
        });

        // ============================================
        // 10. TOAST NOTIFICATIONS (Premium)
        // ============================================
        
        function showToast(title, message, type) {
            const iconMap = {
                success: '✅',
                error: '❌',
                warning: '⚠️',
                info: 'ℹ️'
            };

            const toastHtml = `
                <div class="toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0 show" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="d-flex">
                        <div class="toast-body">
                            <strong>${iconMap[type] || ''} ${title}</strong> ${message}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                </div>
            `;

            let $container = $('.toast-container');
            if (!$container.length) {
                $('body').append('<div class="toast-container position-fixed top-0 end-0 p-3" style="z-index:9999;"></div>');
                $container = $('.toast-container');
            }

            const $toast = $(toastHtml);
            $container.append($toast);

            setTimeout(function() {
                $toast.fadeOut(400, function() {
                    $(this).remove();
                });
            }, 5000);

            const toastEl = $toast[0];
            if (toastEl) {
                const bsToast = new bootstrap.Toast(toastEl);
                bsToast.show();
            }
        }

        window.showToast = showToast;

        // ============================================
        // 11. NEWSLETTER SUBSCRIPTION (AJAX)
        // ============================================
        
        $('#newsletter-form, #sidebar-newsletter-form').on('submit', function(e) {
            e.preventDefault();
            const $form = $(this);
            const $emailInput = $form.find('input[name="email"]');
            const email = $emailInput.val().trim();
            const $button = $form.find('button[type="submit"]');
            const originalText = $button.html();

            // Email validation
            if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                showToast('Error', 'Please enter a valid email address.', 'error');
                $emailInput.addClass('is-invalid');
                return;
            }
            $emailInput.removeClass('is-invalid');

            // Disable button and show loading
            $button.prop('disabled', true);
            $button.html('<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Subscribing...');

            $.ajax({
                url: $form.attr('action'),
                method: 'POST',
                data: {
                    email: email,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                dataType: 'json',
                success: function(response) {
                    $emailInput.val('');
                    showToast('Success!', 'You have been subscribed to our newsletter.', 'success');
                },
                error: function(xhr) {
                    let message = 'Failed to subscribe. Please try again.';
                    if (xhr.responseJSON && xhr.responseJSON.message) {
                        message = xhr.responseJSON.message;
                    }
                    showToast('Error!', message, 'error');
                },
                complete: function() {
                    $button.prop('disabled', false);
                    $button.html(originalText);
                }
            });
        });

        // ============================================
        // 12. DARK MODE TOGGLE
        // ============================================
        
        const $darkModeToggle = $('#dark-mode-toggle');
        if ($darkModeToggle.length) {
            const savedDarkMode = localStorage.getItem('darkMode');
            if (savedDarkMode === 'true') {
                $('body').addClass('dark-mode');
                $darkModeToggle.find('i').removeClass('fa-moon').addClass('fa-sun');
            }

            const darkModeMedia = window.matchMedia('(prefers-color-scheme: dark)');
            darkModeMedia.addEventListener('change', function(e) {
                if (!localStorage.getItem('darkMode')) {
                    if (e.matches) {
                        $('body').addClass('dark-mode');
                        $darkModeToggle.find('i').removeClass('fa-moon').addClass('fa-sun');
                    } else {
                        $('body').removeClass('dark-mode');
                        $darkModeToggle.find('i').removeClass('fa-sun').addClass('fa-moon');
                    }
                }
            });

            $darkModeToggle.on('click', function() {
                $('body').toggleClass('dark-mode');
                const isDark = $('body').hasClass('dark-mode');
                localStorage.setItem('darkMode', isDark);
                $(this).find('i').toggleClass('fa-moon fa-sun');

                const message = isDark ? 'Dark mode enabled' : 'Light mode enabled';
                const $announcer = $('#aria-announcer');
                if ($announcer.length) {
                    $announcer.text(message);
                }
            });
        }

        // ============================================
        // 13. INFINITE SCROLL
        // ============================================
        
        let page = 1;
        const $loading = $('#loading');
        const $postsContainer = $('#posts-container');
        let isLoading = false;
        let hasMore = true;
        let throttleTimer = false;

        if ($loading.length && $postsContainer.length) {
            $(window).on('scroll', function() {
                if (throttleTimer) return;
                throttleTimer = true;
                setTimeout(function() {
                    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 300) {
                        if (!isLoading && hasMore) {
                            loadMorePosts();
                        }
                    }
                    throttleTimer = false;
                }, 200);
            });
        }

        function loadMorePosts() {
            isLoading = true;
            $loading.html('<div class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="text-muted mt-2">Loading more posts...</p></div>').show();
            page++;

            $.ajax({
                url: window.location.pathname,
                data: { page: page },
                success: function(data) {
                    const $newPosts = $(data).find('.post-item');
                    if ($newPosts.length) {
                        $postsContainer.append($newPosts);
                        $newPosts.each(function() {
                            $(this).addClass('fade-in-up').css('opacity', '0');
                            setTimeout(function() {
                                $(this).addClass('revealed').css('opacity', '1');
                            }.bind(this), 100);
                        });
                        $loading.hide();
                        isLoading = false;
                    } else {
                        hasMore = false;
                        $loading.html('<div class="text-center py-4"><p class="text-muted">✨ You\'ve reached the end!</p></div>').show();
                    }
                },
                error: function() {
                    $loading.html('<div class="text-center py-4"><p class="text-danger">❌ Error loading posts. Please refresh.</p></div>').show();
                    isLoading = false;
                }
            });
        }

        // ============================================
        // 14. LIKE & BOOKMARK (Optimistic UI)
        // ============================================
        
        $('.btn-like').on('click', function() {
            const slug = $(this).data('slug');
            const $btn = $(this);
            const $icon = $btn.find('i');
            const $count = $('#likes-count, .likes-count');

            const wasLiked = $icon.hasClass('fas');
            $icon.toggleClass('fas far');
            if ($count.length) {
                let currentCount = parseInt($count.text()) || 0;
                $count.text(wasLiked ? currentCount - 1 : currentCount + 1);
            }

            $.ajax({
                url: '/post/like/' + slug + '/',
                method: 'POST',
                data: {
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    if ($count.length) {
                        $count.text(response.total_likes);
                    }
                    if (response.liked) {
                        $icon.addClass('fas');
                        $btn.addClass('active');
                        $btn.addClass('pulse');
                        setTimeout(function() {
                            $btn.removeClass('pulse');
                        }, 500);
                    } else {
                        $icon.removeClass('fas');
                        $btn.removeClass('active');
                    }
                },
                error: function() {
                    $icon.toggleClass('fas far');
                    if ($count.length) {
                        let currentCount = parseInt($count.text()) || 0;
                        $count.text(wasLiked ? currentCount + 1 : currentCount - 1);
                    }
                    showToast('Error', 'Failed to like the post. Please try again.', 'error');
                }
            });
        });

        $('.btn-bookmark').on('click', function() {
            const slug = $(this).data('slug');
            const $btn = $(this);
            const $icon = $btn.find('i');

            const wasBookmarked = $icon.hasClass('fas');
            $icon.toggleClass('fas far');

            $.ajax({
                url: '/post/bookmark/' + slug + '/',
                method: 'POST',
                data: {
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function() {
                    if ($icon.hasClass('fas')) {
                        showToast('Success!', 'Post bookmarked!', 'success');
                        $btn.addClass('active');
                    } else {
                        showToast('Info', 'Bookmark removed.', 'info');
                        $btn.removeClass('active');
                    }
                },
                error: function() {
                    $icon.toggleClass('fas far');
                    showToast('Error', 'Failed to bookmark. Please try again.', 'error');
                }
            });
        });

        // ============================================
        // 15. COMMENT SYSTEM
        // ============================================
        
        $('.reply-btn').on('click', function() {
            const commentId = $(this).data('comment-id');
            const $form = $('#comment-form');
            const $textarea = $form.find('textarea');
            const author = $('#comment-' + commentId + ' strong').text();

            if ($textarea.length) {
                $textarea.val('@' + author + ' ');
                $textarea.focus();

                $form.find('input[name="parent_id"]').remove();
                $('<input>').attr({
                    type: 'hidden',
                    name: 'parent_id',
                    value: commentId
                }).appendTo($form);

                $('html, body').animate({
                    scrollTop: $form.offset().top - 100
                }, 500);

                $form.addClass('bg-light p-3 rounded border border-primary');
                setTimeout(function() {
                    $form.removeClass('bg-light p-3 rounded border border-primary');
                }, 3000);
            }
        });

        $('.vote-comment').on('click', function() {
            const commentId = $(this).data('comment-id');
            const voteType = $(this).data('vote-type');
            const $btn = $(this);

            $.ajax({
                url: '/api/comment-vote/',
                method: 'POST',
                data: {
                    comment_id: commentId,
                    vote_type: voteType,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    if (response.success) {
                        const $votes = $btn.closest('.comment-votes').find('.vote-count');
                        $votes.text(response.votes);
                        showToast('Success', 'Vote recorded!', 'success');
                    }
                },
                error: function() {
                    showToast('Error', 'Failed to vote. Please try again.', 'error');
                }
            });
        });

        setTimeout(function() {
            $('.alert').fadeOut(400, function() {
                $(this).alert('close');
            });
        }, 5000);

        // ============================================
        // 16. SEARCH AUTOCOMPLETE
        // ============================================
        
        const $searchInput = $('input[name="q"]');
        if ($searchInput.length) {
            let debounceTimer;

            $searchInput.on('input', function() {
                clearTimeout(debounceTimer);
                const query = $(this).val().trim();

                if (query.length >= 2) {
                    debounceTimer = setTimeout(function() {
                        const $suggestions = $('.search-suggestions');
                        $suggestions.html('<div class="text-muted p-2"><span class="spinner-border spinner-border-sm me-2" role="status"></span> Searching...</div>').show();

                        $.ajax({
                            url: '/api/search-autocomplete/',
                            data: { q: query },
                            success: function(data) {
                                const $suggestions = $('.search-suggestions');
                                if (data.length) {
                                    let html = '<div class="list-group">';
                                    data.forEach(function(item) {
                                        html += '<a href="/post/' + item.value + '/" class="list-group-item list-group-item-action">' + item.label + '</a>';
                                    });
                                    html += '</div>';
                                    $suggestions.html(html).show();
                                } else {
                                    $suggestions.html('<div class="text-muted p-2">No results found</div>').show();
                                }
                            },
                            error: function() {
                                $('.search-suggestions').html('<div class="text-muted p-2">Search unavailable</div>').show();
                            }
                        });
                    }, 300);
                } else {
                    $('.search-suggestions').hide();
                }
            });

            $(document).on('click', function(e) {
                if (!$(e.target).closest('.search-container, form.d-flex').length) {
                    $('.search-suggestions').hide();
                }
            });

            $searchInput.on('keydown', function(e) {
                if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                    e.preventDefault();
                    const $items = $('.search-suggestions .list-group-item');
                    if ($items.length) {
                        const currentIndex = $items.index($items.filter('.active'));
                        let newIndex = e.key === 'ArrowDown' ? currentIndex + 1 : currentIndex - 1;
                        if (newIndex < 0) newIndex = $items.length - 1;
                        if (newIndex >= $items.length) newIndex = 0;
                        $items.removeClass('active').eq(newIndex).addClass('active');
                    }
                }
                if (e.key === 'Enter') {
                    const $active = $('.search-suggestions .list-group-item.active');
                    if ($active.length) {
                        window.location.href = $active.attr('href');
                    }
                }
            });
        }

        // ============================================
        // 17. POST PREVIEW
        // ============================================
        
        $('#preview-post').on('click', function() {
            const content = $('#id_content').val();
            const title = $('#id_title').val();

            $('#preview-modal .modal-title').text(title || 'Post Preview');
            $('#preview-modal .modal-body').html(
                content || '<p class="text-muted">No content to preview.</p>'
            );
            const modal = new bootstrap.Modal(document.getElementById('preview-modal'));
            modal.show();
        });

        // ============================================
        // 18. COUNTER ANIMATION
        // ============================================
        
        $('.counter').each(function() {
            const $el = $(this);
            const target = parseInt($el.data('target') || $el.text());
            const duration = 1500;
            const startTime = performance.now();

            function updateCounter(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = Math.round(eased * target);
                $el.text(current);

                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    $el.text(target);
                }
            }

            if ('IntersectionObserver' in window) {
                const observer = new IntersectionObserver(function(entries) {
                    if (entries[0].isIntersecting) {
                        requestAnimationFrame(updateCounter);
                        observer.unobserve(this);
                    }
                }.bind(this));
                observer.observe(this);
            } else {
                requestAnimationFrame(updateCounter);
            }
        });

        // ============================================
        // 19. KEYBOARD ACCESSIBILITY
        // ============================================
        
        $(document).on('keydown', function(e) {
            // ESC - Close modals, dropdowns
            if (e.key === 'Escape') {
                const openModals = document.querySelectorAll('.modal.show');
                openModals.forEach(function(modal) {
                    const bsModal = bootstrap.Modal.getInstance(modal);
                    if (bsModal) {
                        bsModal.hide();
                    }
                });
                $('.dropdown-menu.show').removeClass('show');
                $('.search-suggestions').hide();
            }

            // Ctrl+K / Cmd+K - Focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const $search = $('input[name="q"]');
                if ($search.length) {
                    $search.focus();
                    $search.select();
                }
            }

            // Ctrl+Shift+D - Toggle dark mode
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'D') {
                e.preventDefault();
                const $toggle = $('#dark-mode-toggle');
                if ($toggle.length) {
                    $toggle.trigger('click');
                }
            }
        });

        // ============================================
        // 20. ACTIVE NAV HIGHLIGHT
        // ============================================
        
        const currentPath = window.location.pathname;
        $('.navbar .nav-link').each(function() {
            const $link = $(this);
            const href = $link.attr('href');
            
            if (href) {
                if (href === currentPath || href === window.location.href) {
                    $link.addClass('active');
                } else if (href !== '/' && currentPath.startsWith(href) && href.length > 1) {
                    $link.addClass('active');
                } else if (href === '/' && currentPath === '/') {
                    $link.addClass('active');
                }
            }
        });

        // ============================================
        // 21. RIPPLE EFFECT (Buttons)
        // ============================================
        
        $('.btn').on('click', function(e) {
            const $btn = $(this);
            if ($btn.is(':disabled')) return;

            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const size = Math.max(rect.width, rect.height);

            const $ripple = $('<span class="ripple"></span>').css({
                width: size,
                height: size,
                left: x - size / 2,
                top: y - size / 2
            });

            $btn.append($ripple);
            setTimeout(function() {
                $ripple.remove();
            }, 600);
        });

        // ============================================
        // 22. COPY TO CLIPBOARD
        // ============================================
        
        $('.copy-btn').on('click', function() {
            const text = $(this).data('copy-text');
            if (text) {
                navigator.clipboard.writeText(text)
                    .then(function() {
                        showToast('Success', 'Copied to clipboard!', 'success');
                    })
                    .catch(function() {
                        // Fallback
                        const textarea = document.createElement('textarea');
                        textarea.value = text;
                        document.body.appendChild(textarea);
                        textarea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textarea);
                        showToast('Success', 'Copied to clipboard!', 'success');
                    });
            }
        });

        // ============================================
        // 23. REDUCED MOTION SUPPORT
        // ============================================
        
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        if (prefersReducedMotion.matches) {
            $('.fade-in, .fade-in-up, .fade-in-down, .hover-card, .tag-badge').css({
                'animation': 'none',
                'transition': 'none'
            });
            $(document).on('scroll', function() {
                $('.fade-in-up, .fade-in-down').css('opacity', '1');
            });
        }

        // ============================================
        // 24. ARIA ANNOUNCER
        // ============================================
        
        if (!$('#aria-announcer').length) {
            $('<div id="aria-announcer" aria-live="polite" aria-atomic="true" style="position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;"></div>')
                .appendTo('body');
        }

        // ============================================
        // 25. PAGE TRANSITION
        // ============================================
        
        $('body').addClass('page-loaded');

        // ============================================
        // 26. CONSOLE WELCOME
        // ============================================
        
        console.log('%c✨ MyBlog', 'font-size:24px; font-weight:bold; color:#2563EB;');
        console.log('%cBuilt with ❤️ using Django & Bootstrap', 'font-size:14px; color:#64748B;');

    }); // END DOCUMENT READY

    // ============================================
    // 27. WINDOW LOAD
    // ============================================
    
    $(window).on('load', function() {
        $('.spinner-overlay').fadeOut(400, function() {
            $(this).remove();
        });

        $('.fade-in, .fade-in-up, .fade-in-down').each(function() {
            const $el = $(this);
            if (!$el.hasClass('revealed')) {
                $el.css('opacity', '1');
                $el.addClass('revealed');
            }
        });
    });

})(jQuery);