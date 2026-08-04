/**
 * ============================================
 * PROFESSIONAL BLOG JAVASCRIPT v4.0
 * COMPLETE ENHANCEMENTS
 * ============================================
 */

(function($) {
    'use strict';

    $(document).ready(function() {

        // ============================================
        // 1. BOOTSTRAP INITIALIZATION
        // ============================================
        
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
            new bootstrap.Tooltip(el, { trigger: 'hover focus', placement: 'top', delay: { show: 100, hide: 100 } });
        });

        document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => {
            new bootstrap.Popover(el, { trigger: 'click', placement: 'bottom', delay: { show: 100, hide: 100 } });
        });

        document.querySelectorAll('[data-bs-toggle="dropdown"]').forEach(el => {
            new bootstrap.Dropdown(el, {
                popperConfig: function(config) {
                    return { ...config, modifiers: [...config.modifiers, { name: 'offset', options: { offset: [0, 8] } }] };
                }
            });
        });

        document.querySelectorAll('[data-bs-toggle="modal"]').forEach(el => {
            const target = el.dataset.bsTarget || el.getAttribute('href');
            if (target && target.startsWith('#')) {
                const modalEl = document.querySelector(target);
                if (modalEl) new bootstrap.Modal(modalEl, { backdrop: true, keyboard: true, focus: true });
            }
        });

        // ============================================
        // 2. NAVBAR SCROLL EFFECT
        // ============================================
        
        const navbar = document.querySelector('.navbar');
        let lastScroll = 0;

        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
            
            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            if (currentScroll > 200 && currentScroll > lastScroll) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            lastScroll = currentScroll;
        }, { passive: true });

        // ============================================
        // 3. BACK TO TOP
        // ============================================
        
        const backToTop = document.getElementById('back-to-top');
        if (backToTop) {
            window.addEventListener('scroll', function() {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                if (scrollTop > 300) {
                    backToTop.classList.add('visible');
                } else {
                    backToTop.classList.remove('visible');
                }
            }, { passive: true });

            backToTop.addEventListener('click', function() {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        }

        // ============================================
        // 4. READING PROGRESS BAR
        // ============================================
        
        const progressBar = document.getElementById('reading-progress');
        if (progressBar) {
            window.addEventListener('scroll', function() {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                const docHeight = document.documentElement.scrollHeight - window.innerHeight;
                const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
                progressBar.style.width = Math.min(progress, 100) + '%';
            }, { passive: true });
        }

        // ============================================
        // 5. LAZY LOADING IMAGES
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
            }, { rootMargin: '100px 0px', threshold: 0.01 });

            document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img));
        }

        // ============================================
        // 6. SCROLL REVEAL ANIMATIONS
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
            }, { threshold: 0.1, rootMargin: '20px 0px' });

            document.querySelectorAll('.reveal, .post-item, .card, .stat-card, .dashboard-card').forEach(el => {
                el.style.opacity = '0';
                revealObserver.observe(el);
            });
        }

        // ============================================
        // 7. FORM VALIDATION
        // ============================================
        
        document.querySelectorAll('.needs-validation').forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!this.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                this.classList.add('was-validated');
            }, false);
        });

        // ============================================
        // 8. CHARACTER COUNTER
        // ============================================
        
        document.querySelectorAll('textarea[maxlength]').forEach(textarea => {
            const maxLength = parseInt(textarea.getAttribute('maxlength'));
            const counter = document.createElement('span');
            counter.className = 'char-counter text-muted small ms-2';
            
            const parent = textarea.closest('.form-group, .mb-3');
            if (parent) parent.appendChild(counter);
            else textarea.insertAdjacentElement('afterend', counter);

            function updateCounter() {
                const remaining = maxLength - textarea.value.length;
                counter.textContent = remaining + ' characters remaining';
                counter.style.color = remaining < 20 ? '#DC2626' : '#64748B';
            }

            textarea.addEventListener('input', updateCounter);
            updateCounter();
        });

        // ============================================
        // 9. IMAGE PREVIEW
        // ============================================
        
        document.querySelectorAll('input[type="file"]').forEach(input => {
            input.addEventListener('change', function() {
                const file = this.files[0];
                if (file && file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    const preview = this.closest('.form-group, .mb-3')?.querySelector('.image-preview');
                    if (preview) {
                        reader.onload = function(e) {
                            preview.innerHTML = '<img src="' + e.target.result + '" class="img-fluid rounded mt-2" style="max-height:200px;object-fit:cover;border:1px solid #E2E8F0;">';
                            preview.style.display = 'block';
                        };
                        reader.readAsDataURL(file);
                    }
                }
            });
        });

        // ============================================
        // 10. TOAST NOTIFICATIONS
        // ============================================
        
        function showToast(title, message, type) {
            const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
            
            let container = document.querySelector('.toast-container');
            if (!container) {
                container = document.createElement('div');
                container.className = 'toast-container position-fixed top-0 end-0 p-3';
                container.style.zIndex = '9999';
                document.body.appendChild(container);
            }

            const toast = document.createElement('div');
            toast.className = 'toast align-items-center text-white bg-' + (type === 'success' ? 'success' : 'danger') + ' border-0 show';
            toast.setAttribute('role', 'alert');
            toast.setAttribute('aria-live', 'assertive');
            toast.setAttribute('aria-atomic', 'true');
            
            toast.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        <strong>${icons[type] || ''} ${title}</strong> ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            `;
            
            container.appendChild(toast);
            
            setTimeout(() => {
                toast.style.transition = 'opacity 0.4s ease';
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 400);
            }, 5000);
        }

        window.showToast = showToast;

        // ============================================
        // 11. NEWSLETTER SUBSCRIPTION
        // ============================================
        
        document.querySelectorAll('#newsletter-form, #sidebar-newsletter-form, #footer-newsletter-form').forEach(form => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const emailInput = this.querySelector('input[name="email"]');
                const email = emailInput.value.trim();
                const button = this.querySelector('button[type="submit"]');
                const originalText = button.innerHTML;

                if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                    showToast('Error', 'Please enter a valid email address.', 'error');
                    emailInput.classList.add('is-invalid');
                    return;
                }
                emailInput.classList.remove('is-invalid');

                button.disabled = true;
                button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Subscribing...';

                fetch(this.action, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value },
                    body: new FormData(this)
                })
                .then(response => response.json())
                .then(data => {
                    emailInput.value = '';
                    showToast('Success!', data.message || 'You have been subscribed!', 'success');
                })
                .catch(() => {
                    showToast('Error!', 'Failed to subscribe. Please try again.', 'error');
                })
                .finally(() => {
                    button.disabled = false;
                    button.innerHTML = originalText;
                });
            });
        });

        // ============================================
        // 12. LIKE BUTTON
        // ============================================
        
        document.querySelectorAll('.btn-like').forEach(btn => {
            btn.addEventListener('click', function() {
                const slug = this.dataset.slug;
                const icon = this.querySelector('i');
                const countEl = document.querySelector('#likes-count, .likes-count');
                const wasLiked = icon.classList.contains('fas');
                
                icon.classList.toggle('fas');
                icon.classList.toggle('far');
                if (countEl) {
                    let current = parseInt(countEl.textContent) || 0;
                    countEl.textContent = wasLiked ? current - 1 : current + 1;
                }
                
                this.classList.add('heart-beat');
                setTimeout(() => this.classList.remove('heart-beat'), 1000);

                fetch('/post/like/' + slug + '/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value }
                })
                .then(response => response.json())
                .then(data => {
                    if (countEl) countEl.textContent = data.total_likes;
                    if (data.liked) {
                        icon.classList.add('fas');
                        this.classList.add('active');
                    } else {
                        icon.classList.remove('fas');
                        this.classList.remove('active');
                    }
                })
                .catch(() => {
                    icon.classList.toggle('fas');
                    icon.classList.toggle('far');
                    if (countEl) {
                        let current = parseInt(countEl.textContent) || 0;
                        countEl.textContent = wasLiked ? current + 1 : current - 1;
                    }
                    showToast('Error', 'Failed to like the post.', 'error');
                });
            });
        });

        // ============================================
        // 13. BOOKMARK BUTTON
        // ============================================
        
        document.querySelectorAll('.btn-bookmark').forEach(btn => {
            btn.addEventListener('click', function() {
                const slug = this.dataset.slug;
                const icon = this.querySelector('i');
                const wasBookmarked = icon.classList.contains('fas');
                
                icon.classList.toggle('fas');
                icon.classList.toggle('far');
                
                this.classList.add('scale-up');
                setTimeout(() => this.classList.remove('scale-up'), 400);

                fetch('/post/bookmark/' + slug + '/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value }
                })
                .then(() => {
                    if (icon.classList.contains('fas')) {
                        showToast('Success!', 'Post bookmarked!', 'success');
                        this.classList.add('active');
                    } else {
                        showToast('Info', 'Bookmark removed.', 'info');
                        this.classList.remove('active');
                    }
                })
                .catch(() => {
                    icon.classList.toggle('fas');
                    icon.classList.toggle('far');
                    showToast('Error', 'Failed to bookmark.', 'error');
                });
            });
        });

        // ============================================
        // 14. COMMENT REPLY
        // ============================================
        
        document.querySelectorAll('.reply-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const commentId = this.dataset.commentId;
                const form = document.querySelector('#comment-form');
                const textarea = form?.querySelector('textarea');
                const author = document.querySelector('#comment-' + commentId + ' strong')?.textContent || '';
                
                if (textarea) {
                    textarea.value = '@' + author + ' ';
                    textarea.focus();
                    
                    form.querySelector('input[name="parent_id"]')?.remove();
                    
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'parent_id';
                    input.value = commentId;
                    form.appendChild(input);
                    
                    window.scrollTo({ top: form.offsetTop - 100, behavior: 'smooth' });
                }
            });
        });

        // ============================================
        // 15. AUTO-DISMISS ALERTS
        // ============================================
        
        setTimeout(() => {
            document.querySelectorAll('.alert').forEach(alert => {
                setTimeout(() => {
                    alert.style.transition = 'opacity 0.4s ease';
                    alert.style.opacity = '0';
                    setTimeout(() => alert.remove(), 400);
                }, 5000);
            });
        }, 100);

        // ============================================
        // 16. KEYBOARD ACCESSIBILITY
        // ============================================
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.querySelectorAll('.modal.show').forEach(modal => {
                    const bsModal = bootstrap.Modal.getInstance(modal);
                    if (bsModal) bsModal.hide();
                });
                document.querySelectorAll('.dropdown-menu.show').forEach(el => el.classList.remove('show'));
                document.querySelector('.search-suggestions')?.style.setProperty('display', 'none');
            }
            
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.querySelector('input[name="q"]')?.focus();
            }
        });

        // ============================================
        // 17. ACTIVE NAV HIGHLIGHT
        // ============================================
        
        const currentPath = window.location.pathname;
        document.querySelectorAll('.navbar .nav-link').forEach(link => {
            const href = link.getAttribute('href');
            if (href) {
                if (href === currentPath || (href !== '/' && currentPath.startsWith(href) && href.length > 1) || (href === '/' && currentPath === '/')) {
                    link.classList.add('active');
                }
            }
        });

        // ============================================
        // 18. RIPPLE EFFECT
        // ============================================
        
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                if (this.disabled) return;
                
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                ripple.style.width = size + 'px';
                ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                
                this.appendChild(ripple);
                ripple.addEventListener('animationend', () => ripple.remove());
            });
        });

        // ============================================
        // 19. COPY TO CLIPBOARD
        // ============================================
        
        document.querySelectorAll('.copy-btn, .copy-link').forEach(btn => {
            btn.addEventListener('click', function() {
                const text = this.dataset.copyText || this.dataset.url || window.location.href;
                if (text) {
                    navigator.clipboard.writeText(text)
                        .then(() => {
                            const originalText = this.innerHTML;
                            this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                            showToast('Success', 'Copied to clipboard!', 'success');
                            setTimeout(() => { this.innerHTML = originalText; }, 2000);
                        })
                        .catch(() => {
                            const textarea = document.createElement('textarea');
                            textarea.value = text;
                            document.body.appendChild(textarea);
                            textarea.select();
                            document.execCommand('copy');
                            textarea.remove();
                            showToast('Success', 'Copied to clipboard!', 'success');
                        });
                }
            });
        });

        // ============================================
        // 20. NEWSLETTER POPUP
        // ============================================

        function showNewsletterPopup() {
            const popup = document.getElementById('newsletter-popup');
            const isShown = localStorage.getItem('newsletter_shown');
            
            if (popup && !isShown) {
                setTimeout(function() {
                    popup.classList.add('active');
                    localStorage.setItem('newsletter_shown', 'true');
                }, 5000);
            }
        }

        window.closePopup = function() {
            const popup = document.getElementById('newsletter-popup');
            if (popup) {
                popup.classList.remove('active');
                setTimeout(function() {
                    popup.style.display = 'none';
                }, 500);
            }
        };

        $(document).on('click', function(e) {
            const popup = document.getElementById('newsletter-popup');
            if (popup && popup.classList.contains('active')) {
                if (!$(e.target).closest('.popup-content, .popup-close').length) {
                    closePopup();
                }
            }
        });

        $(document).on('keydown', function(e) {
            if (e.key === 'Escape') {
                closePopup();
            }
        });

        $(document).on('click', '.popup-close', function() {
            closePopup();
        });

        $('#newsletter-popup form').on('submit', function(e) {
            e.preventDefault();
            const form = $(this);
            const email = form.find('input[name="email"]').val();
            const button = form.find('button[type="submit"]');
            const originalText = button.html();

            if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                showToast('Error', 'Please enter a valid email address.', 'error');
                return;
            }

            button.prop('disabled', true);
            button.html('<span class="spinner-border spinner-border-sm me-2" role="status"></span> Subscribing...');

            $.ajax({
                url: form.attr('action'),
                method: 'POST',
                data: {
                    email: email,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                dataType: 'json',
                success: function(response) {
                    showToast('Success!', 'You have been subscribed to our newsletter!', 'success');
                    form.find('input[name="email"]').val('');
                    setTimeout(closePopup, 1000);
                },
                error: function(xhr) {
                    let message = 'Failed to subscribe. Please try again.';
                    if (xhr.responseJSON && xhr.responseJSON.message) {
                        message = xhr.responseJSON.message;
                    }
                    showToast('Error!', message, 'error');
                },
                complete: function() {
                    button.prop('disabled', false);
                    button.html(originalText);
                }
            });
        });

        // Initialize popup
        if (!localStorage.getItem('newsletter_shown')) {
            setTimeout(function() {
                const popup = document.getElementById('newsletter-popup');
                if (popup) {
                    popup.classList.add('active');
                    localStorage.setItem('newsletter_shown', 'true');
                }
            }, 5000);
        }

        $(document).on('touchstart', function(e) {
            const popup = document.getElementById('newsletter-popup');
            if (popup && popup.classList.contains('active')) {
                if (!$(e.target).closest('.popup-content, .popup-close').length) {
                    closePopup();
                }
            }
        });

        let scrollTimeout;
        $(window).on('scroll', function() {
            const popup = document.getElementById('newsletter-popup');
            if (popup && popup.classList.contains('active')) {
                clearTimeout(scrollTimeout);
                scrollTimeout = setTimeout(function() {
                    closePopup();
                }, 2000);
            }
        });

        // ============================================
        // 21. POST PREVIEW
        // ============================================
        
        document.querySelector('#preview-post')?.addEventListener('click', function() {
            const content = document.querySelector('#id_content')?.value || '';
            const title = document.querySelector('#id_title')?.value || 'Post Preview';
            const modal = document.querySelector('#preview-modal');
            if (modal) {
                modal.querySelector('.modal-title').textContent = title;
                modal.querySelector('.modal-body').innerHTML = content || '<p class="text-muted">No content to preview.</p>';
                new bootstrap.Modal(modal).show();
            }
        });

        // ============================================
        // 22. CONFIRM DELETE
        // ============================================
        
        window.confirmDelete = function(url, message) {
            message = message || 'Are you sure you want to delete this item? This action cannot be undone.';
            if (confirm(message)) {
                window.location.href = url;
            }
        };

        // ============================================
        // 23. REDUCED MOTION
        // ============================================
        
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.querySelectorAll('.fade-in, .fade-in-up, .fade-in-down, .hover-card, .tag-badge').forEach(el => {
                el.style.animation = 'none';
                el.style.transition = 'none';
            });
        }

        // ============================================
        // 24. ARIA ANNOUNCER
        // ============================================
        
        if (!document.querySelector('#aria-announcer')) {
            const announcer = document.createElement('div');
            announcer.id = 'aria-announcer';
            announcer.setAttribute('aria-live', 'polite');
            announcer.setAttribute('aria-atomic', 'true');
            announcer.style.cssText = 'position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;';
            document.body.appendChild(announcer);
        }

        // ============================================
        // 25. CONSOLE WELCOME
        // ============================================
        
        console.log('%c✨ PixelPost', 'font-size:24px; font-weight:bold; color:#2563EB;');
        console.log('%cBuilt with ❤️ using Django & Bootstrap', 'font-size:14px; color:#64748B;');

    });

    // ============================================
    // 26. WINDOW LOAD
    // ============================================
    
    window.addEventListener('load', function() {
        document.querySelector('.spinner-overlay')?.remove();
        
        document.querySelectorAll('.fade-in, .fade-in-up, .fade-in-down').forEach(el => {
            if (!el.classList.contains('revealed')) {
                el.style.opacity = '1';
                el.classList.add('revealed');
            }
        });
    });

})(jQuery);

// ============================================
// MOBILE FIXES
// ============================================

// Close navbar on link click (mobile)
$(document).ready(function() {
    $('.navbar .nav-link').on('click', function() {
        if ($(window).width() <= 992) {
            $('.navbar-collapse').collapse('hide');
        }
    });
    
    // Fix for iOS Safari 100vh issue
    function setVH() {
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', vh + 'px');
    }
    setVH();
    window.addEventListener('resize', setVH);
});

// Smooth scroll for mobile
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const offsetTop = target.offsetTop - 70;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        }
    });
});