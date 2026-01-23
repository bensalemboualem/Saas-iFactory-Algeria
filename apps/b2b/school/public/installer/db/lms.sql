-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 02, 2023 at 05:30 AM
-- Server version: 8.0.29
-- PHP Version: 8.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ins_lms`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ac_name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ac_number` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `branch` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `balance` double(16,2) NOT NULL DEFAULT '0.00',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `is_default` tinyint NOT NULL DEFAULT '0' COMMENT '0 = no, 1 = yes',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `name`, `ac_name`, `ac_number`, `code`, `branch`, `balance`, `status_id`, `is_default`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'Account 1', 'John Doe', '123456789', '123456789', 'California', 0.00, 1, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `app_home_sections`
--

CREATE TABLE `app_home_sections` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `snake_title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order` int NOT NULL DEFAULT '1',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `app_home_sections`
--

INSERT INTO `app_home_sections` (`id`, `title`, `snake_title`, `order`, `status_id`, `type`, `is_delete`, `created_at`, `updated_at`) VALUES
(1, 'Slider', 'slider', 1, 1, 'api', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Categories', 'Categories', 2, 1, 'api', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'Featured Courses', 'featured_courses', 3, 1, 'api', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'Latest Courses', 'latest_courses', 4, 1, 'api', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(5, 'Best Rated Course', 'best_rated_courses', 5, 1, 'api', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(6, 'Best Selling Course', 'best_selling_courses', 6, 1, 'api', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(7, 'Free Courses', 'free_courses', 7, 1, 'api', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(8, 'Discounted Courses', 'discount_courses', 8, 1, 'api', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(9, 'Slider', 'slider', 1, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(10, 'Featured Courses', 'featured_courses', 2, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(11, 'Popular Category', 'popular_category', 3, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(12, 'Latest Courses', 'latest_courses', 4, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(13, 'Best Rated Course', 'best_rated_courses', 5, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(14, 'Most Popular Course', 'most_popular_courses', 6, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(15, 'Discounted Courses', 'discount_courses', 7, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(16, 'Become An Instructor', 'become_an_instructor', 8, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(17, 'Testimonials', 'testimonials', 9, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(18, 'Our Recent Blogs', 'blogs', 10, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(19, 'Trusted By Thousands', 'brands', 11, 1, 'web', 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `assignments`
--

CREATE TABLE `assignments` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `course_id` bigint UNSIGNED DEFAULT NULL,
  `details` longtext COLLATE utf8mb4_unicode_ci,
  `assignment_file` bigint UNSIGNED DEFAULT NULL,
  `marks` double(8,2) NOT NULL DEFAULT '0.00',
  `pass_marks` double(8,2) NOT NULL DEFAULT '0.00',
  `deadline` timestamp NULL DEFAULT NULL,
  `note` longtext COLLATE utf8mb4_unicode_ci,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '21',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `is_notify` tinyint NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `point` double(8,2) NOT NULL DEFAULT '0.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `assignments`
--

INSERT INTO `assignments` (`id`, `title`, `course_id`, `details`, `assignment_file`, `marks`, `pass_marks`, `deadline`, `note`, `status_id`, `created_by`, `updated_by`, `is_notify`, `created_at`, `updated_at`, `point`) VALUES
(1, 'Assignment 1', 1, 'Assignment 1', NULL, 100.00, 40.00, '2023-05-08 23:30:32', NULL, 22, 5, NULL, 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32', 100.00),
(2, 'Assignment 2', 1, 'Assignment 2', NULL, 100.00, 40.00, '2023-05-08 23:30:32', NULL, 22, 5, NULL, 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32', 100.00),
(3, 'Assignment 3', 1, 'Assignment 3', NULL, 100.00, 40.00, '2023-05-08 23:30:32', NULL, 21, 5, NULL, 0, '2023-05-01 23:30:32', '2023-05-01 23:30:32', 100.00);

-- --------------------------------------------------------

--
-- Table structure for table `assignment_submits`
--

CREATE TABLE `assignment_submits` (
  `id` bigint UNSIGNED NOT NULL,
  `assignment_id` bigint UNSIGNED DEFAULT NULL,
  `enroll_id` bigint UNSIGNED DEFAULT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `marks` double(8,2) NOT NULL DEFAULT '0.00',
  `total_marks` double(8,2) NOT NULL DEFAULT '0.00',
  `point` double(8,2) NOT NULL DEFAULT '0.00',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '3',
  `details` longtext COLLATE utf8mb4_unicode_ci,
  `assignment_file` bigint UNSIGNED DEFAULT NULL,
  `is_reviewed` tinyint(1) NOT NULL DEFAULT '0',
  `is_submitted` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blogs`
--

CREATE TABLE `blogs` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_id` bigint UNSIGNED DEFAULT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `blog_categories_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_by` bigint UNSIGNED DEFAULT NULL,
  `meta_title` longtext COLLATE utf8mb4_unicode_ci,
  `meta_description` longtext COLLATE utf8mb4_unicode_ci,
  `meta_keywords` longtext COLLATE utf8mb4_unicode_ci,
  `meta_image_id` bigint UNSIGNED DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `blogs`
--

INSERT INTO `blogs` (`id`, `title`, `slug`, `description`, `image_id`, `status_id`, `blog_categories_id`, `created_by`, `updated_by`, `deleted_by`, `meta_title`, `meta_description`, `meta_keywords`, `meta_image_id`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'How to Leverage an LMS During the COVID-19 Global Pandemic', 'how-to-leverage-an-lms-during-the-covid-19-global-pandemic-YE666b24', '<p>There have been all kinds disease outbreaks since the turn of the new millennium—the SARS coronavirus (2002-2004), the MERS coronavirus (starting in 2012), and the Ebola epidemic (2013-2016), just to name a few. What’s unprecedented about the COVID-19 coronavirus global pandemic is how fast it’s spreading all over the world. Although most people can get through having the virus and the disease it causes without any issues, the real problem is with the elderly and those with underlying medical conditions.</p><p>Get our free course ‘<a href=\"https://knowledgeessentials.eleapcourses.com/protecting-yourself-against-covid-19-and-other-contagious-illnesses-111959.html\"><i>Protecting Yourself Against COVID-19 and Other Contagious Illnesses</i></a><i>‘ </i>to help protect you, your team or your loved ones.</p><p><img src=\"https://www.eleapsoftware.com/wp-content/uploads/2020/03/how-to-leverage-an-lms-during-the-covid-19-global-pandemic-2000x1358.jpg.webp\" alt=\"How to Leverage an LMS During the COVID-19 Global Pandemic\" srcset=\"https://www.eleapsoftware.com/wp-content/uploads/2020/03/how-to-leverage-an-lms-during-the-covid-19-global-pandemic-2000x1358.jpg.webp 2000w,  https://www.eleapsoftware.com/wp-content/uploads/2020/03/how-to-leverage-an-lms-during-the-covid-19-global-pandemic-300x204.jpg.webp 300w,  https://www.eleapsoftware.com/wp-content/uploads/2020/03/how-to-leverage-an-lms-during-the-covid-19-global-pandemic-768x522.jpg.webp 768w,  https://www.eleapsoftware.com/wp-content/uploads/2020/03/how-to-leverage-an-lms-during-the-covid-19-global-pandemic-1536x1043.jpg.webp 1536w,  https://www.eleapsoftware.com/wp-content/uploads/2020/03/how-to-leverage-an-lms-during-the-covid-19-global-pandemic-2048x1391.jpg.webp 2048w\" sizes=\"100vw\" width=\"2000\"></p><p>But stopping a virus that spreads as fast as the COVID-19 coronavirus requires taking drastic measures. Schools are shutting down at an alarming rate, public gatherings and events of all kinds are being cancelled, and many workplaces are having as many employees as possible work from home. For companies everywhere, now is the time to creatively leverage a learning management system (LMS) like eLeaP to keep help keep your business operating.</p><h2><strong>An LMS is Uniquely Suited to Help During the COVID-19 Pandemic</strong></h2><p>Of course your company has email for communicating with employees working from home, and all kinds of video conference apps for having live meetings, but both of those technologies have their limitations. Your workers need to see their leaders and managers, not just read messages from them, but video conferencing isn’t a good solution for large-scale communication given the challenges of having everyone participate at the same time. This is when you could leverage the power of an easy-to-use LMS like <a href=\"https://www.eleapsoftware.com/\">eLeaP</a> to get business-critical messaging across to your employees without everyone having to be online at the same moment.</p><p>eLeaP’s <a href=\"https://www.eleapsoftware.com/comprehensive-learning-management-system/\">comprehensive features</a> were designed to be a simple yet powerful solution that makes uploading and distributing video content extremely fast and easy. The company CEO, other C-suite executives, managers, and team leaders can quickly record videos, get them uploaded into the LMS, and designate who needs to be notified the content is there and ready to be watched.</p><h2><strong>Let an LMS be Your HR Tool During the Pandemic</strong></h2><p>Your company’s HR professionals are going to be among the most hard-pressed staff during the COVID-19 pandemic. Workers are going to have all kinds of questions about how remote working is going to happen, how their pay may or may not be affected, what the expectations are in terms of hours and availability, and all sorts of other questions. What’s the best way to begin assembling resources, guides, and messaging to address all these HR issues? Once again it’s an LMS that has capability to quickly house and distribute all this information. Whether it’s video content recorded by HR staff, PDFs, PowerPoint slide decks, or even just audio recordings, a well-designed LMS can handle all these different types of content and make them immediately available to everyone or to designated users as needed.</p><h2><strong>During a Business Slow-Down, Use an LMS for Training and Upskilling</strong></h2><p>How the COVID-19 global pandemic affects any given business is going to vary widely from company to company, and even by different types of workers and employees within companies. In some cases, whether working from home or not, some employees may not see any change at all in the volume of work they do on a day-to-day basis. In other cases, however, a slow-down in the business may mean there’s simply not as much to do for some workers.</p><p>This is when you can engage in additional eLearning through an LMS for the training programs there previously never seemed to be time for doing. For employees who have less to do, this could be the time when they can engage in significant upskilling and additional training. When the COVID-19 pandemic ends and businesses get back to normal operations, you’ll have a workforce that’s ready to do more to get the company back on track and moving forward.</p><h2><strong>Keeping the COVID-19 Pandemic in Perspective</strong></h2><p>Everyone is feeling anxious about the huge disruption to life and work being caused by the drastic measures that must be taken to slow the spread of the COVID-19 coronavirus. After all, we were experiencing the longest post-recession economic recovery in history. There can be no doubt that this global pandemic is going to push the economy into a recession. Businesses are going to be impacted, some more than others, but no business will go unscathed during this crisis.</p><p>What’s important to keep in mind is this: Everyone, and I do mean everyone—every single business and every single employee with in every business—has a responsibility to do everything we can to protect the most vulnerable people in society, meaning the ones who will be killed by COVID-19 if they become infected. Keep this in mind when you’re feeling the negative business impacts of the pandemic. There are lives at stake if we don’t handle this right, and that means prioritizing people’s lives over and above the business, as difficult as that is. We are literally all in this together, and we will get through this crisis together!</p><p>If your company hasn’t yet adopted an LMS, now is the time to get it done. While we normally recommend a thorough process for assessing your company’s needs before selecting an LMS vendor, time is of the essence in the midst of a global pandemic. What we can tell you with confidence is this: The eLeaP LMS is extremely user-friendly. In fact, it’s been ranked #9 on Capterra’s Top 20 Most User-Friendly LMS Software list for several years in a row. And it’s incredibly easy to get up and running with eLeaP—literally in a matter of minutes.</p><p>eLeaP is a cloud-based LMS, which means there’s no software to download and install. All you need is your favorite electronic device (desktop, laptop, tablet, smartphone) with an internet connection and a web browser. We offer a <a href=\"https://www.eleapsoftware.com/free-trial/\">free trial</a> where you can start using eLeaP right away to see for yourself, and at the end of the free trial, you’ll appreciate the very <a href=\"https://www.eleapsoftware.com/pricing/\">affordable monthly pricing</a> based on the number of users.</p>', NULL, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Are You an LMS Skeptic?', 'are-you-an-lms-skeptic-K9wF4frK', '<p>There are hundreds of different learning management system (LMS) solutions available to businesses today but if you are an LMS skeptic, this <a href=\"https://www.eleapsoftware.com/whitepaper/the-skeptics-guide-to-lms-ebook/\">free eBook</a> is for you. With so many vendors out there, you’d think most businesses have probably jumped onto the LMS bandwagon. And yet there still many companies that don’t have an LMS. For whatever reason, they are what you might call LMS skeptics. Are you an <a href=\"https://www.eleapsoftware.com/whitepaper/the-skeptics-guide-to-lms-ebook/\">LMS skeptic</a>? If so, this is a must-read article for you.</p><p><img src=\"https://www.eleapsoftware.com/wp-content/uploads/2020/03/lms-skeptic-are-you-1024x819.jpg.webp\" alt=\"Are you an LMS skeptic?\" srcset=\"https://www.eleapsoftware.com/wp-content/uploads/2020/03/lms-skeptic-are-you-1024x819.jpg.webp 1024w,  https://www.eleapsoftware.com/wp-content/uploads/2020/03/lms-skeptic-are-you-300x240.jpg.webp 300w,  https://www.eleapsoftware.com/wp-content/uploads/2020/03/lms-skeptic-are-you-768x614.jpg.webp 768w,  https://www.eleapsoftware.com/wp-content/uploads/2020/03/lms-skeptic-are-you-1536x1229.jpg.webp 1536w,  https://www.eleapsoftware.com/wp-content/uploads/2020/03/lms-skeptic-are-you-2048x1638.jpg.webp 2048w,  https://www.eleapsoftware.com/wp-content/uploads/2020/03/lms-skeptic-are-you-1568x1254.jpg.webp 1568w\" sizes=\"100vw\" width=\"1024\"></p><p><strong>The Ever-Growing Number of LMS Vendors</strong></p><p>Trying to figure out just how many different LMS options are out there is a daunting task because there are just so many of them. If you were to create a list of all the different corporate LMS options available for businesses, do you know how many would be on it? More than 640! There surely wouldn’t be so many different companies making and selling LMS software if there isn’t a real need for it, right? But you’re an LMS skeptic, and the true skeptic doesn’t do something just because everyone else is doing it!</p><p><strong>LMS Dissatisfaction is Still High</strong></p><p>Maybe you’ve also seen the many articles published online over the years that present data on how many companies are unhappy with their LMS. The most recent data on this is quite interesting. It comes from a research project at ATD (the Association for Talent Development). Their research team asked the important question, <a href=\"https://www.td.org/research-reports/is-the-lms-dead\">Is the LMS Dead?</a> The answer was no, it’s alive and well, but get a load of these statistics:</p><ul><li><i><strong>Only 9%</strong></i> of companies surveyed were able to say their LMS was highly effective.</li><li><i><strong>Around 33%</strong></i> said employee users found the company LMS “difficult” to use (which is just a nice way of saying they hate it).</li><li><i><strong>Nearly 50%</strong></i> said the user interface of their LMS was not appealing.</li></ul><p>As an LMS skeptic, you’re probably thinking you’ve made the right choice in <i>not</i> adopting an LMS. But you’d be wrong. Just because a bunch of companies haven’t found the right LMS doesn’t mean it’s entirely unavailable. And if you stubbornly refuse to find the right LMS for your company, you’ll be missing out on the ways an LMS can boost learning and training, which has an impact on your bottom line.</p><p><strong>The Skeptic’s Guide to LMS</strong></p><p>We wanted to design a resource that would speak directly to the LMS skeptic. The goal was to explain as clearly as possible what an LMS can and cannot do for a company. An LMS isn’t a magic bullet, it’s a management tool with a relatively narrowly defined purpose and scope. If you understand what an LMS can do while not expecting it to do more than is possible, you will see how an LMS really can improve the way learning and training happens in your company. If you’re an LMS skeptic, then we invite you to get your copy of <a href=\"https://www.eleapsoftware.com/whitepaper/the-skeptics-guide-to-lms-ebook/\"><strong>The Skeptic’s Guide to LMS</strong></a>. And who knows? When you’re finished reading it, you might just find you’re ready to find the right LMS for your company. Here’s a sneak preview of the guide’s contents:</p><ul><li>6 Signs You Need an LMS Solution</li><li>What an LMS Can and Cannot do for Your Company</li><li>How to Craft a Winning LMS-Enabled Learning and Training Strategy</li><li>How to Maximize Your ROI</li></ul><p>Get your copy of <a href=\"https://www.eleapsoftware.com/whitepaper/the-skeptics-guide-to-lms-ebook/\"><strong>The Skeptic’s Guide to LMS</strong></a>&nbsp;now!</p>', NULL, 1, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'LMS Software for the 21st Century: A Guide to eLearning Solutions', 'lms-software-for-the-21st-century-a-guide-to-elearning-solutions-OGt7FqNQ', '<p>The demand for online learning solutions is constantly growing and evolving. As such, the available solutions need to do the same. When you have a larger audience and you need to convey a lot of information in an easy-to-access format, eLearning through an LMS software (<a href=\"https://www.eleapsoftware.com/comprehensive-learning-management-system/\">LMS Learning Management System)</a> presents the ideal solution. It is important, however, to take the time to get to know the various resources that are available and see what they have to offer. By taking a deeper look at the benefits and uses of these platforms, it may be easier to see what your company stands to gain from employing technology as a teaching tool.</p><p><img src=\"https://www.eleapsoftware.com/wp-content/uploads/2020/02/A-Guide-to-eLearning-Solutions--1024x696.jpg.webp\" alt=\"LMS Learning Management Systems to take care of the toughest challenges\" srcset=\"https://www.eleapsoftware.com/wp-content/uploads/2020/02/A-Guide-to-eLearning-Solutions--1024x696.jpg.webp 1024w,  https://www.eleapsoftware.com/wp-content/uploads/2020/02/A-Guide-to-eLearning-Solutions--300x204.jpg.webp 300w,  https://www.eleapsoftware.com/wp-content/uploads/2020/02/A-Guide-to-eLearning-Solutions--768x522.jpg.webp 768w,  https://www.eleapsoftware.com/wp-content/uploads/2020/02/A-Guide-to-eLearning-Solutions--1536x1043.jpg.webp 1536w,  https://www.eleapsoftware.com/wp-content/uploads/2020/02/A-Guide-to-eLearning-Solutions--2048x1391.jpg.webp 2048w,  https://www.eleapsoftware.com/wp-content/uploads/2020/02/A-Guide-to-eLearning-Solutions--1568x1065.jpg.webp 1568w\" sizes=\"100vw\" width=\"1024\"></p><p><strong>The eLearning Industry</strong></p><p>There are literally thousands of vendors and companies promoting their own LMS software solutions today. That can make it a challenge to figure out which platforms are going to be best for the job at hand. In fact, in 2021, it is expected that this market will be worth close to $16 billion, with the majority of the revenue generated in North America.</p><p>Studies have shown that over 40% of the global Fortune 500 companies out there are now using some type of online learning to help instruct employees with formal <a href=\"https://www.eleapsoftware.com/on-the-job-training-why-ojt-matters/\">job training</a> and other educational needs. With the growing trend of online learning, it’s expected that as many as half of all available college courses are now online or somehow based in eLearning technology. It’s becoming glaringly obvious that the growing demand for virtual learning systems is there and that companies need to get on board.</p><p>The eLearning industry is changing the way people look at skill acquisition and job training. The ability to implement and manage a learning solution virtually can save companies a lot of time and money on their training efforts. Of course, because there are so many different solutions out there, it is important to take the time to explore the industry and find the solutions that work best for your specific training needs. Keep reading to learn more about LMS platforms and what you should be getting from them, as well as how you can use them to revolutionize your own training programs.</p><p><strong>LMS-What It Means to You</strong></p><p>Simply put, an LMS software is a <a href=\"https://www.eleapsoftware.com/learning-management-system/\">Learning Management System</a> or an integrated platform that is designed to organize and manage training materials and educational courses, providing a user-friendly interface through which people can access the materials and courses. These platforms are typically hosted online and cloud-based, making them easy to modify, adapt, and access for everyone in the organization. This system is designed to make training easier, so if you find that you are struggling to actualize that goal, you might be going at things from the wrong direction.</p><p>Just because you have and use an LMS doesn’t mean that you’re making the best use of it, after all. Some people are employing these systems without a full understanding of what they offer or they simply roll out the first LMS software that they find without taking the time to do their homework and figure out which systems are actually going to be best for their needs. Fortunately, this guide has all of the insights and information that you need to ensure that you capitalize on your investment in a learning management system, no matter what type of training you have that needs to be done.</p><p><strong>Features of a Strong LMS Platform</strong></p><p>There are definitely some things that you should be looking for when you’re investing in an LMS software solution for your e-learning needs. There are a seemingly endless number of features available on various platforms, but you really need to take the time to figure out which features are most important to you. Do you know what you are looking for? If you are trying to make the most of your investment in this training tool, here are some big features that you really need to think about.</p><p><i>Data Migration</i></p><p>Your online learning platform should be able to move and integrate data seamlessly. Whether you are just investing in a new system and merging your previous LMS data or you are just trying to keep things integrated, the migration process in the software that you choose should provide you with all of the resources that you need to keep everything in one place.</p><p><i>Built-in Social Media Support</i></p><p>People are social creatures by nature. Now that social media plays such a large role in careers and other parts of life, having social media support and integration can be a value-added asset to any LMS. You can often incorporate social media groups and blogs that allow users to connect and work with their peers, as well as social tracking tools that will help you keep an eye on things like participation and engagement.</p><p><i>Gamification (Badges, etc.)</i></p><p>Who doesn’t love a good competition? People are naturally competitive and if you give them the tools to gamify their learning, they are going to feel more accomplished and be more likely to succeed. Motivating people is easier when you have points, leaderboards, and other tools that appeal to the competitive nature of people. When you choose a platform with these features, you’re giving people a fun way to learn and challenge themselves while also challenging their peers.</p><p><i>Reporting and Analytics Tools</i></p><p>It does no good to have the best LMS in place if you don’t know how it’s doing or how well the training is going for your employees. Any software worth its weight is going to include reporting and analytics tools, and the best ones will have customizable reporting options. While pre-built reports are nice, you are also going to have specific metrics that you want to track that other companies might not think about. That’s why having a robust platform that offers pre-planned reports and customized reporting together is the best solution.</p><p><i>Collaborative Learning Resources</i></p><p>Although eLearning is a rather effective means of training, there is definitely something to be said for taking a collaborative approach, as well. Some people experience the best learning in social media groups, online discussions, and other collaborations. Even if most of your training is a solo activity, you should still have engaging tools that allow people to collaborate and communicate during the training process. If your platform doesn’t have integrated collaborative tools, you should at least make sure that it has the option for plug-ins or add-ons so that you can capitalize on these resources in the event that you need them.</p><p><i>Branding and Corporate Integration</i></p><p>While it might not occur to you that something like your logo and company name could impact the quality of your training materials, you really need that cohesion across the board. People might not need to see the logo on every single training page, but having a branded, personalized training program that incorporates this can definitely give people the sense of cohesiveness that they expect from online training programs that are offered at a professional level.</p><p><i>Personalized Learning</i></p><p>The ability to provide your employees with personalized learning solutions is invaluable when you employ the use of an LMS platform. Everyone knows that “one size fits all” training is not effective in any situation. Some programs will allow you to create unique non-linear courses or personalized paths to learning for your trainees to help them learn the things that they may be missing. You can customize this to people’s specific gaps or areas where they struggle to ensure that you address what people need the most.</p><p><i>Easy-to-Use Interface</i></p><p>Finally, there is no value to an LMS software that isn’t easy for people to use. It doesn’t matter how well the rest of the features work or how many other checkboxes are marked off when you invest in one of these tools. The fact of the matter is that if the platform isn’t intuitive and user-friendly, it’s not going to be successful. Make sure that you test out the platform for yourself and do so from the perspective of the least-experienced Internet or computer user. That way, you’ll know that it’s the best solution and that everyone can use it to succeed with their eLearning programs.</p><p><i>Cloud-Based Learning</i></p><p>Although most LMS software platforms are already cloud-based, there are some installed software programs available, as well. Of course, hard-installed systems won’t have as much flexibility and customization. Plus, cloud-based systems are easier to change and update, and you can allow users to access the information from just about anywhere that they desire. While cloud-based learning isn’t absolutely necessary, it certainly makes things easier. Imagine if you lose connectivity in the office or if people suddenly decide they need to check in on a training module while they’re at home. Having a cloud-based solution with access from just about anywhere can make the difference. Plus, then when you need to scale up or down, or change anything in the LMS, you aren’t investing in expensive new hardware upgrades or other costs because everything is virtual and easy to scale.</p><p><i>Accessibility Across Devices</i></p><p>Although you might only have your team training in the office, having access to the LMS platform across devices can help your team. You should choose a platform that is responsive and can be accessed across a variety of devices just in case you need smartphone or tablet access for any reason. Plus, then your trainees will be able to come back and access training resources whenever they need them. Imagine that you find yourself in a situation where the Internet is down and you still want to get the training done. Having an LMS platform that offers offline connectivity can save you from a wasted day. These are all things that are important to think about, even if they may not seem like pressing issues. The more prepared you are, the better your eLearning will be. The right platform can make all the difference.</p><p><i>Customized Support 24/7</i></p><p>The most important thing with any LMS is being able to get help when it isn’t working as it should, or in the event that you need assistance for anything. Can you reach your support team via phone, email, and/or live chat? Make sure that you ask about support services <strong>before</strong> you commit to a solution. You should also check reviews and see what other users say about ongoing support. The company might be on the ball when you are ready to sign up to work with them, but will they offer the same resources and support when you have paid for the services? That’s where it really counts.</p>', NULL, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'How to Improve Company Culture', 'how-to-improve-company-culture-7pgFL9mq', '<p>Having a strong company culture is not merely a good idea, it is essential in today’s business world. You might be in a position where you realize that your company culture needs to improve. Everything that is happening within the company, including the way that employees deal with one another and with clients and customers is a part of the company culture. The <a href=\"https://www.eleapsoftware.com/free-training-resources/developing-a-learning-culture-white-paper/\">culture</a> is the “norms” of the company and how things get done. Everyone should feel happy, comfortable, and welcome if you have a <a href=\"https://www.eleapsoftware.com/the-secret-to-creating-a-company-culture-that-embraces-learning/\">positive company culture</a>.</p><p><img src=\"https://www.eleapsoftware.com/wp-content/uploads/2020/01/improve-culture-workplace-1024x683.jpg.webp\" alt=\"How to improve workplace culture\" srcset=\"https://www.eleapsoftware.com/wp-content/uploads/2020/01/improve-culture-workplace-1024x683.jpg.webp 1024w,  https://www.eleapsoftware.com/wp-content/uploads/2020/01/improve-culture-workplace-300x200.jpg.webp 300w,  https://www.eleapsoftware.com/wp-content/uploads/2020/01/improve-culture-workplace-768x512.jpg.webp 768w,  https://www.eleapsoftware.com/wp-content/uploads/2020/01/improve-culture-workplace-1536x1024.jpg.webp 1536w,  https://www.eleapsoftware.com/wp-content/uploads/2020/01/improve-culture-workplace-2048x1365.jpg.webp 2048w,  https://www.eleapsoftware.com/wp-content/uploads/2020/01/improve-culture-workplace-1568x1045.jpg.webp 1568w\" sizes=\"100vw\" width=\"1024\"></p><p>Of course, creating a great company culture is not always easy to do and you might not know the best methods and strategies to consider. The following are some tips that you will want to employ.</p><h3>Improve Trust in the Company</h3><p>How much do your employees trust the company? If you are overly secretive about changes being made at the company that will affect the employees, trust will erode. While there may be certain things that you cannot divulge to the employees, being as transparent in other areas is very important. If there are important changes coming, make sure that the managers and the employees are a part of this conversation as early as possible.</p><p>Make sure that everyone in the company knows the core values, as well. Transparency helps to build better relationships in the company, and it can make sure that everyone is aligned in their goals and values. It also allows for better and more engagement.</p><h3>Become More Flexible</h3><p>In some companies, there are still rigid and traditional company cultures that tend not to work well in the modern environment. Becoming more flexible and accommodating for the employees can provide massive improvements to the way that people feel about the company and their role within it. Offering flexible hours and work schedules can often be helpful.</p><h3>Create Strong Coworker Connections</h3><p>People who are in the workplace should feel like they belong there, and they should feel as if they are a part of the team. Those companies that have people who all have the same goals, and who feel as if they are part of a larger team are going to be more productive. By incorporating team-building activities and team outings, it can help to foster this type of connection between the coworkers.</p><p>Of course, when creating those outings, it is important to think about the people who are in the company. Not everyone wants to go out to a happy hour with the rest of the team. Not everyone can get away after the end of the workday for a movie because they have to think about their family at home. You want to have opportunities that everyone will be able to participate in without feeling as though they are being excluded.</p><h3>Everyone Should Have a Voice</h3><p>It is important that everyone in the workplace feel as if they have a voice that will be heard. Workplaces are diverse locations where people may not always feel as if they can voice their opinion regarding work, of they may feel as if it will not be heard. It is essential that the company culture is welcoming to everyone and that all employees know that their contributions are important and heard.</p><p>Managers should always hear everyone out whether the idea is good or bad. Otherwise, there is a chance that they could miss out on an idea that could help to take care of problems that exist or that could improve the company in some other way.</p><h3>Understand the Dangers of Burning Out</h3><p>One of the aspects of the workplace that does not always get enough attention is the concept of burnout amongst employees. When employees are feeling burned out, not only are they not going to be as productive to the company, but it can even create a bad environment for the other employees at the company. Understand how the employees work best and make sure that they have the flexibility they need, as mentioned above. Sometimes, changing up the work schedules or reducing the workload is necessary.</p><h3>Allow for Employee Feedback</h3><p>Even if you believe that there is nothing wrong with your company culture, you might not be seeing the entire picture. Those who are working in HR or who are managers are not always down “in the trenches” with everyone else. They do not always see everything that goes on, both good and bad. Therefore, the employees need to have a way to provide feedback about the job and their coworkers. Make it easy for the employees to speak with representatives from human resources, and make sure they understand that they can do so anonymously if needed.</p><h3>Recognition and Reward</h3><p>Another part of the company culture that can help to bring people together is to provide recognition and rewards for when individuals and teams do well. There are many ways that employees can be rewarded. They could be provided with a gift card, with a paid day off, a trip to a spa or movie, etc. This creates a more positive environment, and it helps to provide incentives that other employees will want to earn for themselves.</p><h3>Perform Culture Audits of the Company</h3><p>Even after you believe that you have improved the company culture, your work is not done. This is an ongoing project, and occasionally, you will need to audit and take an honest look at the company culture and how it might have changed in the past six months. Certain employees, for example, might be making life miserable for other employees, and you won’t always know this unless you are proactive with your audits. There needs to be maintenance to your company culture, and sometimes, it will need to evolve with the times.</p><p>What is the current company culture at your company like? If you are looking for ways that you can improve things at your company, the above tips will help you to <a href=\"https://www.inc.com/dan-scalco/4-ways-to-vastly-improve-your-company-culture.html\">create a culture</a> that ensures you are staying true to your core values and brand, and that the employees are happy.</p>', NULL, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `blog_categories`
--

CREATE TABLE `blog_categories` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `blog_categories`
--

INSERT INTO `blog_categories` (`id`, `title`, `slug`, `status_id`, `created_by`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Blog Category one', 'blog-category-one', 1, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Blog Category two', 'blog-category-two', 1, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `bookmarks`
--

CREATE TABLE `bookmarks` (
  `id` bigint UNSIGNED NOT NULL,
  `course_id` bigint UNSIGNED DEFAULT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bookmarks`
--

INSERT INTO `bookmarks` (`id`, `course_id`, `user_id`, `created_at`, `updated_at`) VALUES
(1, 1, 4, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 2, 4, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 3, 4, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `brands`
--

CREATE TABLE `brands` (
  `id` bigint UNSIGNED NOT NULL,
  `serial` bigint UNSIGNED NOT NULL,
  `image_id` bigint UNSIGNED DEFAULT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_by` bigint UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `brands`
--

INSERT INTO `brands` (`id`, `serial`, `image_id`, `status_id`, `created_by`, `updated_by`, `deleted_by`, `created_at`, `updated_at`) VALUES
(1, 1, NULL, 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 2, NULL, 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 3, NULL, 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 4, NULL, 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(5, 5, NULL, 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `carts`
--

CREATE TABLE `carts` (
  `id` bigint UNSIGNED NOT NULL,
  `course_id` bigint UNSIGNED DEFAULT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `certificate_generates`
--

CREATE TABLE `certificate_generates` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `upload_id` bigint UNSIGNED DEFAULT NULL,
  `enroll_id` bigint UNSIGNED NOT NULL,
  `issue_date` timestamp NOT NULL DEFAULT '2023-05-01 23:30:31',
  `certificate_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `certificate_templates`
--

CREATE TABLE `certificate_templates` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_id` bigint UNSIGNED DEFAULT NULL,
  `text` text COLLATE utf8mb4_unicode_ci,
  `is_rtl` tinyint NOT NULL DEFAULT '0',
  `default_id` bigint UNSIGNED NOT NULL DEFAULT '10',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `font_id` bigint UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `certificate_templates`
--

INSERT INTO `certificate_templates` (`id`, `title`, `image_id`, `text`, `is_rtl`, `default_id`, `status_id`, `font_id`, `created_at`, `updated_at`) VALUES
(1, 'Certificate of Completion', NULL, 'This is to certify that [name] has successfully completed the course [course] on [date].', 0, 11, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `countries`
--

CREATE TABLE `countries` (
  `id` bigint UNSIGNED NOT NULL,
  `phone` varchar(6) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code` char(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `symbol` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `currency` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `countries`
--

INSERT INTO `countries` (`id`, `phone`, `code`, `name`, `symbol`, `currency`, `created_at`, `updated_at`) VALUES
(1, '93', 'AF', 'Afghanistan', '؋', 'AFN', NULL, NULL),
(2, '358', 'AX', 'Aland Islands', '€', 'EUR', NULL, NULL),
(3, '355', 'AL', 'Albania', 'Lek', 'ALL', NULL, NULL),
(4, '213', 'DZ', 'Algeria', 'دج', 'DZD', NULL, NULL),
(5, '1684', 'AS', 'American Samoa', '$', 'USD', NULL, NULL),
(6, '376', 'AD', 'Andorra', '€', 'EUR', NULL, NULL),
(7, '244', 'AO', 'Angola', 'Kz', 'AOA', NULL, NULL),
(8, '1264', 'AI', 'Anguilla', '$', 'XCD', NULL, NULL),
(9, '672', 'AQ', 'Antarctica', '$', 'AAD', NULL, NULL),
(10, '1268', 'AG', 'Antigua and Barbuda', '$', 'XCD', NULL, NULL),
(11, '54', 'AR', 'Argentina', '$', 'ARS', NULL, NULL),
(12, '374', 'AM', 'Armenia', '֏', 'AMD', NULL, NULL),
(13, '297', 'AW', 'Aruba', 'ƒ', 'AWG', NULL, NULL),
(14, '61', 'AU', 'Australia', '$', 'AUD', NULL, NULL),
(15, '43', 'AT', 'Austria', '€', 'EUR', NULL, NULL),
(16, '994', 'AZ', 'Azerbaijan', 'm', 'AZN', NULL, NULL),
(17, '1242', 'BS', 'Bahamas', 'B$', 'BSD', NULL, NULL),
(18, '973', 'BH', 'Bahrain', '.د.ب', 'BHD', NULL, NULL),
(19, '880', 'BD', 'Bangladesh', '৳', 'BDT', NULL, NULL),
(20, '1246', 'BB', 'Barbados', 'Bds$', 'BBD', NULL, NULL),
(21, '375', 'BY', 'Belarus', 'Br', 'BYN', NULL, NULL),
(22, '32', 'BE', 'Belgium', '€', 'EUR', NULL, NULL),
(23, '501', 'BZ', 'Belize', '$', 'BZD', NULL, NULL),
(24, '229', 'BJ', 'Benin', 'CFA', 'XOF', NULL, NULL),
(25, '1441', 'BM', 'Bermuda', '$', 'BMD', NULL, NULL),
(26, '975', 'BT', 'Bhutan', 'Nu.', 'BTN', NULL, NULL),
(27, '591', 'BO', 'Bolivia', 'Bs.', 'BOB', NULL, NULL),
(28, '599', 'BQ', 'Bonaire, Sint Eustatius and Saba', '$', 'USD', NULL, NULL),
(29, '387', 'BA', 'Bosnia and Herzegovina', 'KM', 'BAM', NULL, NULL),
(30, '267', 'BW', 'Botswana', 'P', 'BWP', NULL, NULL),
(31, '55', 'BV', 'Bouvet Island', 'kr', 'NOK', NULL, NULL),
(32, '55', 'BR', 'Brazil', 'R$', 'BRL', NULL, NULL),
(33, '246', 'IO', 'British Indian Ocean Territory', '$', 'USD', NULL, NULL),
(34, '673', 'BN', 'Brunei Darussalam', 'B$', 'BND', NULL, NULL),
(35, '359', 'BG', 'Bulgaria', 'Лв.', 'BGN', NULL, NULL),
(36, '226', 'BF', 'Burkina Faso', 'CFA', 'XOF', NULL, NULL),
(37, '257', 'BI', 'Burundi', 'FBu', 'BIF', NULL, NULL),
(38, '855', 'KH', 'Cambodia', 'KHR', 'KHR', NULL, NULL),
(39, '237', 'CM', 'Cameroon', 'FCFA', 'XAF', NULL, NULL),
(40, '1', 'CA', 'Canada', '$', 'CAD', NULL, NULL),
(41, '238', 'CV', 'Cape Verde', '$', 'CVE', NULL, NULL),
(42, '1345', 'KY', 'Cayman Islands', '$', 'KYD', NULL, NULL),
(43, '236', 'CF', 'Central African Republic', 'FCFA', 'XAF', NULL, NULL),
(44, '235', 'TD', 'Chad', 'FCFA', 'XAF', NULL, NULL),
(45, '56', 'CL', 'Chile', '$', 'CLP', NULL, NULL),
(46, '86', 'CN', 'China', '¥', 'CNY', NULL, NULL),
(47, '61', 'CX', 'Christmas Island', '$', 'AUD', NULL, NULL),
(48, '672', 'CC', 'Cocos (Keeling) Islands', '$', 'AUD', NULL, NULL),
(49, '57', 'CO', 'Colombia', '$', 'COP', NULL, NULL),
(50, '269', 'KM', 'Comoros', 'CF', 'KMF', NULL, NULL),
(51, '242', 'CG', 'Congo', 'FC', 'XAF', NULL, NULL),
(52, '242', 'CD', 'Congo, Democratic Republic of the Congo', 'FC', 'CDF', NULL, NULL),
(53, '682', 'CK', 'Cook Islands', '$', 'NZD', NULL, NULL),
(54, '506', 'CR', 'Costa Rica', '₡', 'CRC', NULL, NULL),
(55, '225', 'CI', 'Cote D\'Ivoire', 'CFA', 'XOF', NULL, NULL),
(56, '385', 'HR', 'Croatia', 'kn', 'HRK', NULL, NULL),
(57, '53', 'CU', 'Cuba', '$', 'CUP', NULL, NULL),
(58, '599', 'CW', 'Curacao', 'ƒ', 'ANG', NULL, NULL),
(59, '357', 'CY', 'Cyprus', '€', 'EUR', NULL, NULL),
(60, '420', 'CZ', 'Czech Republic', 'Kč', 'CZK', NULL, NULL),
(61, '45', 'DK', 'Denmark', 'Kr.', 'DKK', NULL, NULL),
(62, '253', 'DJ', 'Djibouti', 'Fdj', 'DJF', NULL, NULL),
(63, '1767', 'DM', 'Dominica', '$', 'XCD', NULL, NULL),
(64, '1809', 'DO', 'Dominican Republic', '$', 'DOP', NULL, NULL),
(65, '593', 'EC', 'Ecuador', '$', 'USD', NULL, NULL),
(66, '20', 'EG', 'Egypt', 'ج.م', 'EGP', NULL, NULL),
(67, '503', 'SV', 'El Salvador', '$', 'USD', NULL, NULL),
(68, '240', 'GQ', 'Equatorial Guinea', 'FCFA', 'XAF', NULL, NULL),
(69, '291', 'ER', 'Eritrea', 'Nfk', 'ERN', NULL, NULL),
(70, '372', 'EE', 'Estonia', '€', 'EUR', NULL, NULL),
(71, '251', 'ET', 'Ethiopia', 'Nkf', 'ETB', NULL, NULL),
(72, '500', 'FK', 'Falkland Islands (Malvinas)', '£', 'FKP', NULL, NULL),
(73, '298', 'FO', 'Faroe Islands', 'Kr.', 'DKK', NULL, NULL),
(74, '679', 'FJ', 'Fiji', 'FJ$', 'FJD', NULL, NULL),
(75, '358', 'FI', 'Finland', '€', 'EUR', NULL, NULL),
(76, '33', 'FR', 'France', '€', 'EUR', NULL, NULL),
(77, '594', 'GF', 'French Guiana', '€', 'EUR', NULL, NULL),
(78, '689', 'PF', 'French Polynesia', '₣', 'XPF', NULL, NULL),
(79, '262', 'TF', 'French Southern Territories', '€', 'EUR', NULL, NULL),
(80, '241', 'GA', 'Gabon', 'FCFA', 'XAF', NULL, NULL),
(81, '220', 'GM', 'Gambia', 'D', 'GMD', NULL, NULL),
(82, '995', 'GE', 'Georgia', 'ლ', 'GEL', NULL, NULL),
(83, '49', 'DE', 'Germany', '€', 'EUR', NULL, NULL),
(84, '233', 'GH', 'Ghana', 'GH₵', 'GHS', NULL, NULL),
(85, '350', 'GI', 'Gibraltar', '£', 'GIP', NULL, NULL),
(86, '30', 'GR', 'Greece', '€', 'EUR', NULL, NULL),
(87, '299', 'GL', 'Greenland', 'Kr.', 'DKK', NULL, NULL),
(88, '1473', 'GD', 'Grenada', '$', 'XCD', NULL, NULL),
(89, '590', 'GP', 'Guadeloupe', '€', 'EUR', NULL, NULL),
(90, '1671', 'GU', 'Guam', '$', 'USD', NULL, NULL),
(91, '502', 'GT', 'Guatemala', 'Q', 'GTQ', NULL, NULL),
(92, '44', 'GG', 'Guernsey', '£', 'GBP', NULL, NULL),
(93, '224', 'GN', 'Guinea', 'FG', 'GNF', NULL, NULL),
(94, '245', 'GW', 'Guinea-Bissau', 'CFA', 'XOF', NULL, NULL),
(95, '592', 'GY', 'Guyana', '$', 'GYD', NULL, NULL),
(96, '509', 'HT', 'Haiti', 'G', 'HTG', NULL, NULL),
(97, '0', 'HM', 'Heard Island and Mcdonald Islands', '$', 'AUD', NULL, NULL),
(98, '39', 'VA', 'Holy See (Vatican City State)', '€', 'EUR', NULL, NULL),
(99, '504', 'HN', 'Honduras', 'L', 'HNL', NULL, NULL),
(100, '852', 'HK', 'Hong Kong', '$', 'HKD', NULL, NULL),
(101, '36', 'HU', 'Hungary', 'Ft', 'HUF', NULL, NULL),
(102, '354', 'IS', 'Iceland', 'kr', 'ISK', NULL, NULL),
(103, '91', 'IN', 'India', '₹', 'INR', NULL, NULL),
(104, '62', 'ID', 'Indonesia', 'Rp', 'IDR', NULL, NULL),
(105, '98', 'IR', 'Iran, Islamic Republic of', '﷼', 'IRR', NULL, NULL),
(106, '964', 'IQ', 'Iraq', 'د.ع', 'IQD', NULL, NULL),
(107, '353', 'IE', 'Ireland', '€', 'EUR', NULL, NULL),
(108, '44', 'IM', 'Isle of Man', '£', 'GBP', NULL, NULL),
(109, '972', 'IL', 'Israel', '₪', 'ILS', NULL, NULL),
(110, '39', 'IT', 'Italy', '€', 'EUR', NULL, NULL),
(111, '1876', 'JM', 'Jamaica', 'J$', 'JMD', NULL, NULL),
(112, '81', 'JP', 'Japan', '¥', 'JPY', NULL, NULL),
(113, '44', 'JE', 'Jersey', '£', 'GBP', NULL, NULL),
(114, '962', 'JO', 'Jordan', 'ا.د', 'JOD', NULL, NULL),
(115, '7', 'KZ', 'Kazakhstan', 'лв', 'KZT', NULL, NULL),
(116, '254', 'KE', 'Kenya', 'KSh', 'KES', NULL, NULL),
(117, '686', 'KI', 'Kiribati', '$', 'AUD', NULL, NULL),
(118, '850', 'KP', 'Korea, Democratic People\'s Republic of', '₩', 'KPW', NULL, NULL),
(119, '82', 'KR', 'Korea, Republic of', '₩', 'KRW', NULL, NULL),
(120, '381', 'XK', 'Kosovo', '€', 'EUR', NULL, NULL),
(121, '965', 'KW', 'Kuwait', 'ك.د', 'KWD', NULL, NULL),
(122, '996', 'KG', 'Kyrgyzstan', 'лв', 'KGS', NULL, NULL),
(123, '856', 'LA', 'Lao People\'s Democratic Republic', '₭', 'LAK', NULL, NULL),
(124, '371', 'LV', 'Latvia', '€', 'EUR', NULL, NULL),
(125, '961', 'LB', 'Lebanon', '£', 'LBP', NULL, NULL),
(126, '266', 'LS', 'Lesotho', 'L', 'LSL', NULL, NULL),
(127, '231', 'LR', 'Liberia', '$', 'LRD', NULL, NULL),
(128, '218', 'LY', 'Libyan Arab Jamahiriya', 'د.ل', 'LYD', NULL, NULL),
(129, '423', 'LI', 'Liechtenstein', 'CHf', 'CHF', NULL, NULL),
(130, '370', 'LT', 'Lithuania', '€', 'EUR', NULL, NULL),
(131, '352', 'LU', 'Luxembourg', '€', 'EUR', NULL, NULL),
(132, '853', 'MO', 'Macao', '$', 'MOP', NULL, NULL),
(133, '389', 'MK', 'Macedonia, the Former Yugoslav Republic of', 'ден', 'MKD', NULL, NULL),
(134, '261', 'MG', 'Madagascar', 'Ar', 'MGA', NULL, NULL),
(135, '265', 'MW', 'Malawi', 'MK', 'MWK', NULL, NULL),
(136, '60', 'MY', 'Malaysia', 'RM', 'MYR', NULL, NULL),
(137, '960', 'MV', 'Maldives', 'Rf', 'MVR', NULL, NULL),
(138, '223', 'ML', 'Mali', 'CFA', 'XOF', NULL, NULL),
(139, '356', 'MT', 'Malta', '€', 'EUR', NULL, NULL),
(140, '692', 'MH', 'Marshall Islands', '$', 'USD', NULL, NULL),
(141, '596', 'MQ', 'Martinique', '€', 'EUR', NULL, NULL),
(142, '222', 'MR', 'Mauritania', 'MRU', 'MRO', NULL, NULL),
(143, '230', 'MU', 'Mauritius', '₨', 'MUR', NULL, NULL),
(144, '262', 'YT', 'Mayotte', '€', 'EUR', NULL, NULL),
(145, '52', 'MX', 'Mexico', '$', 'MXN', NULL, NULL),
(146, '691', 'FM', 'Micronesia, Federated States of', '$', 'USD', NULL, NULL),
(147, '373', 'MD', 'Moldova, Republic of', 'L', 'MDL', NULL, NULL),
(148, '377', 'MC', 'Monaco', '€', 'EUR', NULL, NULL),
(149, '976', 'MN', 'Mongolia', '₮', 'MNT', NULL, NULL),
(150, '382', 'ME', 'Montenegro', '€', 'EUR', NULL, NULL),
(151, '1664', 'MS', 'Montserrat', '$', 'XCD', NULL, NULL),
(152, '212', 'MA', 'Morocco', 'DH', 'MAD', NULL, NULL),
(153, '258', 'MZ', 'Mozambique', 'MT', 'MZN', NULL, NULL),
(154, '95', 'MM', 'Myanmar', 'K', 'MMK', NULL, NULL),
(155, '264', 'NA', 'Namibia', '$', 'NAD', NULL, NULL),
(156, '674', 'NR', 'Nauru', '$', 'AUD', NULL, NULL),
(157, '977', 'NP', 'Nepal', '₨', 'NPR', NULL, NULL),
(158, '31', 'NL', 'Netherlands', '€', 'EUR', NULL, NULL),
(159, '599', 'AN', 'Netherlands Antilles', 'NAf', 'ANG', NULL, NULL),
(160, '687', 'NC', 'New Caledonia', '₣', 'XPF', NULL, NULL),
(161, '64', 'NZ', 'New Zealand', '$', 'NZD', NULL, NULL),
(162, '505', 'NI', 'Nicaragua', 'C$', 'NIO', NULL, NULL),
(163, '227', 'NE', 'Niger', 'CFA', 'XOF', NULL, NULL),
(164, '234', 'NG', 'Nigeria', '₦', 'NGN', NULL, NULL),
(165, '683', 'NU', 'Niue', '$', 'NZD', NULL, NULL),
(166, '672', 'NF', 'Norfolk Island', '$', 'AUD', NULL, NULL),
(167, '1670', 'MP', 'Northern Mariana Islands', '$', 'USD', NULL, NULL),
(168, '47', 'NO', 'Norway', 'kr', 'NOK', NULL, NULL),
(169, '968', 'OM', 'Oman', '.ع.ر', 'OMR', NULL, NULL),
(170, '92', 'PK', 'Pakistan', '₨', 'PKR', NULL, NULL),
(171, '680', 'PW', 'Palau', '$', 'USD', NULL, NULL),
(172, '970', 'PS', 'Palestinian Territory, Occupied', '₪', 'ILS', NULL, NULL),
(173, '507', 'PA', 'Panama', 'B/.', 'PAB', NULL, NULL),
(174, '675', 'PG', 'Papua New Guinea', 'K', 'PGK', NULL, NULL),
(175, '595', 'PY', 'Paraguay', '₲', 'PYG', NULL, NULL),
(176, '51', 'PE', 'Peru', 'S/.', 'PEN', NULL, NULL),
(177, '63', 'PH', 'Philippines', '₱', 'PHP', NULL, NULL),
(178, '64', 'PN', 'Pitcairn', '$', 'NZD', NULL, NULL),
(179, '48', 'PL', 'Poland', 'zł', 'PLN', NULL, NULL),
(180, '351', 'PT', 'Portugal', '€', 'EUR', NULL, NULL),
(181, '1787', 'PR', 'Puerto Rico', '$', 'USD', NULL, NULL),
(182, '974', 'QA', 'Qatar', 'ق.ر', 'QAR', NULL, NULL),
(183, '262', 'RE', 'Reunion', '€', 'EUR', NULL, NULL),
(184, '40', 'RO', 'Romania', 'lei', 'RON', NULL, NULL),
(185, '70', 'RU', 'Russian Federation', '₽', 'RUB', NULL, NULL),
(186, '250', 'RW', 'Rwanda', 'FRw', 'RWF', NULL, NULL),
(187, '590', 'BL', 'Saint Barthelemy', '€', 'EUR', NULL, NULL),
(188, '290', 'SH', 'Saint Helena', '£', 'SHP', NULL, NULL),
(189, '1869', 'KN', 'Saint Kitts and Nevis', '$', 'XCD', NULL, NULL),
(190, '1758', 'LC', 'Saint Lucia', '$', 'XCD', NULL, NULL),
(191, '590', 'MF', 'Saint Martin', '€', 'EUR', NULL, NULL),
(192, '508', 'PM', 'Saint Pierre and Miquelon', '€', 'EUR', NULL, NULL),
(193, '1784', 'VC', 'Saint Vincent and the Grenadines', '$', 'XCD', NULL, NULL),
(194, '684', 'WS', 'Samoa', 'SAT', 'WST', NULL, NULL),
(195, '378', 'SM', 'San Marino', '€', 'EUR', NULL, NULL),
(196, '239', 'ST', 'Sao Tome and Principe', 'Db', 'STD', NULL, NULL),
(197, '966', 'SA', 'Saudi Arabia', '﷼', 'SAR', NULL, NULL),
(198, '221', 'SN', 'Senegal', 'CFA', 'XOF', NULL, NULL),
(199, '381', 'RS', 'Serbia', 'din', 'RSD', NULL, NULL),
(200, '381', 'CS', 'Serbia and Montenegro', 'din', 'RSD', NULL, NULL),
(201, '248', 'SC', 'Seychelles', 'SRe', 'SCR', NULL, NULL),
(202, '232', 'SL', 'Sierra Leone', 'Le', 'SLL', NULL, NULL),
(203, '65', 'SG', 'Singapore', '$', 'SGD', NULL, NULL),
(204, '1', 'SX', 'Sint Maarten', 'ƒ', 'ANG', NULL, NULL),
(205, '421', 'SK', 'Slovakia', '€', 'EUR', NULL, NULL),
(206, '386', 'SI', 'Slovenia', '€', 'EUR', NULL, NULL),
(207, '677', 'SB', 'Solomon Islands', 'Si$', 'SBD', NULL, NULL),
(208, '252', 'SO', 'Somalia', 'Sh.so.', 'SOS', NULL, NULL),
(209, '27', 'ZA', 'South Africa', 'R', 'ZAR', NULL, NULL),
(210, '500', 'GS', 'South Georgia and the South Sandwich Islands', '£', 'GBP', NULL, NULL),
(211, '211', 'SS', 'South Sudan', '£', 'SSP', NULL, NULL),
(212, '34', 'ES', 'Spain', '€', 'EUR', NULL, NULL),
(213, '94', 'LK', 'Sri Lanka', 'Rs', 'LKR', NULL, NULL),
(214, '249', 'SD', 'Sudan', '.س.ج', 'SDG', NULL, NULL),
(215, '597', 'SR', 'Suriname', '$', 'SRD', NULL, NULL),
(216, '47', 'SJ', 'Svalbard and Jan Mayen', 'kr', 'NOK', NULL, NULL),
(217, '268', 'SZ', 'Swaziland', 'E', 'SZL', NULL, NULL),
(218, '46', 'SE', 'Sweden', 'kr', 'SEK', NULL, NULL),
(219, '41', 'CH', 'Switzerland', 'CHf', 'CHF', NULL, NULL),
(220, '963', 'SY', 'Syrian Arab Republic', 'LS', 'SYP', NULL, NULL),
(221, '886', 'TW', 'Taiwan, Province of China', '$', 'TWD', NULL, NULL),
(222, '992', 'TJ', 'Tajikistan', 'SM', 'TJS', NULL, NULL),
(223, '255', 'TZ', 'Tanzania, United Republic of', 'TSh', 'TZS', NULL, NULL),
(224, '66', 'TH', 'Thailand', '฿', 'THB', NULL, NULL),
(225, '670', 'TL', 'Timor-Leste', '$', 'USD', NULL, NULL),
(226, '228', 'TG', 'Togo', 'CFA', 'XOF', NULL, NULL),
(227, '690', 'TK', 'Tokelau', '$', 'NZD', NULL, NULL),
(228, '676', 'TO', 'Tonga', '$', 'TOP', NULL, NULL),
(229, '1868', 'TT', 'Trinidad and Tobago', '$', 'TTD', NULL, NULL),
(230, '216', 'TN', 'Tunisia', 'ت.د', 'TND', NULL, NULL),
(231, '90', 'TR', 'Turkey', '₺', 'TRY', NULL, NULL),
(232, '7370', 'TM', 'Turkmenistan', 'T', 'TMT', NULL, NULL),
(233, '1649', 'TC', 'Turks and Caicos Islands', '$', 'USD', NULL, NULL),
(234, '688', 'TV', 'Tuvalu', '$', 'AUD', NULL, NULL),
(235, '256', 'UG', 'Uganda', 'USh', 'UGX', NULL, NULL),
(236, '380', 'UA', 'Ukraine', '₴', 'UAH', NULL, NULL),
(237, '971', 'AE', 'United Arab Emirates', 'إ.د', 'AED', NULL, NULL),
(238, '44', 'GB', 'United Kingdom', '£', 'GBP', NULL, NULL),
(239, '1', 'US', 'United States', '$', 'USD', NULL, NULL),
(240, '1', 'UM', 'United States Minor Outlying Islands', '$', 'USD', NULL, NULL),
(241, '598', 'UY', 'Uruguay', '$', 'UYU', NULL, NULL),
(242, '998', 'UZ', 'Uzbekistan', 'лв', 'UZS', NULL, NULL),
(243, '678', 'VU', 'Vanuatu', 'VT', 'VUV', NULL, NULL),
(244, '58', 'VE', 'Venezuela', 'Bs', 'VEF', NULL, NULL),
(245, '84', 'VN', 'Viet Nam', '₫', 'VND', NULL, NULL),
(246, '1284', 'VG', 'Virgin Islands, British', '$', 'USD', NULL, NULL),
(247, '1340', 'VI', 'Virgin Islands, U.s.', '$', 'USD', NULL, NULL),
(248, '681', 'WF', 'Wallis and Futuna', '₣', 'XPF', NULL, NULL),
(249, '212', 'EH', 'Western Sahara', 'MAD', 'MAD', NULL, NULL),
(250, '967', 'YE', 'Yemen', '﷼', 'YER', NULL, NULL),
(251, '260', 'ZM', 'Zambia', 'ZK', 'ZMW', NULL, NULL),
(252, '263', 'ZW', 'Zimbabwe', '$', 'ZWL', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `short_description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `course_category_id` bigint UNSIGNED DEFAULT NULL,
  `requirements` longtext COLLATE utf8mb4_unicode_ci,
  `outcomes` longtext COLLATE utf8mb4_unicode_ci,
  `faq` longtext COLLATE utf8mb4_unicode_ci,
  `tags` longtext COLLATE utf8mb4_unicode_ci,
  `meta_title` longtext COLLATE utf8mb4_unicode_ci,
  `meta_description` longtext COLLATE utf8mb4_unicode_ci,
  `meta_keywords` longtext COLLATE utf8mb4_unicode_ci,
  `meta_author` longtext COLLATE utf8mb4_unicode_ci,
  `meta_image` bigint UNSIGNED DEFAULT NULL,
  `thumbnail` bigint UNSIGNED DEFAULT NULL,
  `course_overview_type` bigint UNSIGNED NOT NULL DEFAULT '17',
  `video_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `language` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'en',
  `course_type` bigint UNSIGNED NOT NULL DEFAULT '13',
  `is_admin` tinyint NOT NULL DEFAULT '11',
  `price` double(16,2) DEFAULT NULL,
  `is_discount` tinyint NOT NULL DEFAULT '10',
  `discount_type` tinyint NOT NULL DEFAULT '1' COMMENT '2 = percentage, 1 = fixed',
  `discount_price` double(16,2) DEFAULT NULL,
  `discount_start_date` date DEFAULT NULL,
  `discount_end_date` date DEFAULT NULL,
  `instructor_id` bigint UNSIGNED DEFAULT NULL,
  `is_multiple_instructor` tinyint NOT NULL DEFAULT '0' COMMENT '0 = false, 1 = true',
  `partner_instructors` json DEFAULT NULL,
  `is_free` tinyint NOT NULL DEFAULT '0' COMMENT '0 = false, 1 = true',
  `level_id` bigint UNSIGNED NOT NULL DEFAULT '18',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '3',
  `visibility_id` bigint UNSIGNED NOT NULL DEFAULT '22',
  `last_modified` timestamp NULL DEFAULT NULL,
  `rating` double NOT NULL DEFAULT '0',
  `total_review` int NOT NULL DEFAULT '0',
  `total_sales` int NOT NULL DEFAULT '0',
  `course_duration` double NOT NULL DEFAULT '0',
  `point` double(8,2) NOT NULL DEFAULT '0.00',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `title`, `slug`, `short_description`, `description`, `course_category_id`, `requirements`, `outcomes`, `faq`, `tags`, `meta_title`, `meta_description`, `meta_keywords`, `meta_author`, `meta_image`, `thumbnail`, `course_overview_type`, `video_url`, `language`, `course_type`, `is_admin`, `price`, `is_discount`, `discount_type`, `discount_price`, `discount_start_date`, `discount_end_date`, `instructor_id`, `is_multiple_instructor`, `partner_instructors`, `is_free`, `level_id`, `status_id`, `visibility_id`, `last_modified`, `rating`, `total_review`, `total_sales`, `course_duration`, `point`, `created_by`, `updated_by`, `deleted_by`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Build a full stack NFT Marketplace using Solidity & Next js', 'build-a-full-stack-nft-marketplace-using-solidity-next-js', 'Learn how to build a full stack NFT marketplace using Solidity, Next js, React js, Web3 js, and IPFS', 'Learn how to build a full stack NFT marketplace using Solidity, Next js, React js, Web3 js, and IPFS', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 15, 'https://youtu.be/3l6Q4QL-j4Q', 'en', 13, 11, 100.00, 11, 1, 20.00, NULL, NULL, NULL, 0, NULL, 0, 18, 1, 22, NULL, 0, 0, 0, 260, 600.00, 5, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'The Complete ChatGPT Web Development Code Along - Javascript', 'the-complete-chatgpt-web-development-code-along-javascript', 'Learn to code with ChatGPT and 10x your Web Development Productivity - Build a MERN Project from scratch with ChatGPT', 'Learn to code with ChatGPT and 10x your Web Development Productivity - Build a MERN Project from scratch with ChatGPT', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2, 15, 'https://youtu.be/3l6Q4QL-j4Q', 'en', 13, 11, NULL, 10, 1, NULL, NULL, NULL, NULL, 0, NULL, 1, 18, 1, 22, NULL, 0, 0, 0, 160, 1000.00, 5, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'The Complete 2023 Web Development Bootcamp', 'the-complete-2023-web-development-bootcamp', 'Become a Full-Stack Web Developer with just ONE course. HTML, CSS, Javascript, Node, React, MongoDB, Web3 and DApps', 'Become a Full-Stack Web Developer with just ONE course. HTML, CSS, Javascript, Node, React, MongoDB, Web3 and DApps', 3, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3, 15, 'https://youtu.be/3l6Q4QL-j4Q', 'en', 13, 11, 160.00, 11, 1, 60.00, NULL, NULL, NULL, 0, NULL, 0, 18, 1, 22, NULL, 0, 0, 0, 0, 0.00, 5, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'The Web Developer Bootcamp 2023', 'the-web-developer-bootcamp-2023', 'The only course you need to learn web development - HTML, CSS, JS, Node, and More!', 'The only course you need to learn web development - HTML, CSS, JS, Node, and More!', 4, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4, 17, 'https://youtu.be/3l6Q4QL-j4Q', 'en', 13, 11, 120.00, 10, 1, NULL, NULL, NULL, NULL, 0, NULL, 0, 18, 1, 22, NULL, 0, 0, 0, 360, 1000.00, 5, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `course_categories`
--

CREATE TABLE `course_categories` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` bigint UNSIGNED DEFAULT NULL,
  `thumbnail` bigint UNSIGNED DEFAULT NULL,
  `parent_id` bigint UNSIGNED DEFAULT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `is_popular` tinyint NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `course_categories`
--

INSERT INTO `course_categories` (`id`, `title`, `slug`, `icon`, `thumbnail`, `parent_id`, `user_id`, `status_id`, `is_popular`, `created_at`, `updated_at`) VALUES
(1, 'Development', 'development', NULL, NULL, NULL, 1, 1, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Web Development', 'web-development', NULL, NULL, 1, 1, 1, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'Mobile Development', 'mobile-development', NULL, NULL, 1, 1, 1, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'Desktop Development', 'desktop-development', NULL, NULL, NULL, 1, 1, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(5, 'Game Development', 'game-development', NULL, NULL, 4, 1, 1, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(6, 'SEO', 'seo', NULL, NULL, 4, 1, 1, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `currencies`
--

CREATE TABLE `currencies` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `symbol` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `currencies`
--

INSERT INTO `currencies` (`id`, `name`, `code`, `symbol`, `created_at`, `updated_at`) VALUES
(1, 'Leke', 'ALL', 'Lek', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(2, 'Dollars', 'USD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(3, 'Afghanis', 'AFN', '؋', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(4, 'Pesos', 'ARS', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(5, 'Guilders', 'AWG', 'ƒ', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(6, 'Dollars', 'AUD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(7, 'New Manats', 'AZN', 'ман', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(8, 'Dollars', 'BSD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(9, 'Dollars', 'BBD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(10, 'Rubles', 'BYR', 'p.', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(11, 'Euro', 'EUR', '€', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(12, 'Dollars', 'BZD', 'BZ$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(13, 'Dollars', 'BMD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(14, 'Bolivianos', 'BOB', '$b', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(15, 'Convertible Marka', 'BAM', 'KM', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(16, 'Pula', 'BWP', 'P', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(17, 'Leva', 'BGN', 'лв', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(18, 'Reais', 'BRL', 'R$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(19, 'Pounds', 'GBP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(20, 'Dollars', 'BND', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(21, 'Riels', 'KHR', '៛', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(22, 'Dollars', 'CAD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(23, 'Dollars', 'KYD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(24, 'Pesos', 'CLP', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(25, 'Yuan Renminbi', 'CNY', '¥', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(26, 'Pesos', 'COP', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(27, 'Colón', 'CRC', '₡', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(28, 'Kuna', 'HRK', 'kn', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(29, 'Pesos', 'CUP', '₱', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(30, 'Koruny', 'CZK', 'Kč', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(31, 'Kroner', 'DKK', 'kr', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(32, 'Pesos', 'DOP ', 'RD$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(33, 'Dollars', 'XCD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(34, 'Pounds', 'EGP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(35, 'Colones', 'SVC', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(36, 'Pounds', 'FKP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(37, 'Dollars', 'FJD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(38, 'Cedis', 'GHC', '¢', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(39, 'Pounds', 'GIP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(40, 'Quetzales', 'GTQ', 'Q', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(41, 'Pounds', 'GGP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(42, 'Dollars', 'GYD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(43, 'Lempiras', 'HNL', 'L', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(44, 'Dollars', 'HKD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(45, 'Forint', 'HUF', 'Ft', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(46, 'Kronur', 'ISK', 'kr', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(47, 'Rupees', 'INR', '₹', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(48, 'Rupiahs', 'IDR', 'Rp', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(49, 'Rials', 'IRR', '﷼', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(50, 'Pounds', 'IMP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(51, 'New Shekels', 'ILS', '₪', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(52, 'Dollars', 'JMD', 'J$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(53, 'Yen', 'JPY', '¥', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(54, 'Pounds', 'JEP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(55, 'Tenge', 'KZT', 'лв', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(56, 'Won', 'KPW', '₩', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(57, 'Won', 'KRW', '₩', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(58, 'Soms', 'KGS', 'лв', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(59, 'Kips', 'LAK', '₭', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(60, 'Lati', 'LVL', 'Ls', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(61, 'Pounds', 'LBP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(62, 'Dollars', 'LRD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(63, 'Switzerland Francs', 'CHF', 'CHF', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(64, 'Litai', 'LTL', 'Lt', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(65, 'Denars', 'MKD', 'ден', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(66, 'Ringgits', 'MYR', 'RM', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(67, 'Rupees', 'MUR', '₨', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(68, 'Pesos', 'MXN', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(69, 'Tugriks', 'MNT', '₮', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(70, 'Meticais', 'MZN', 'MT', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(71, 'Dollars', 'NAD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(72, 'Rupees', 'NPR', '₨', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(73, 'Guilders', 'ANG', 'ƒ', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(74, 'Dollars', 'NZD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(75, 'Cordobas', 'NIO', 'C$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(76, 'Nairas', 'NGN', '₦', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(77, 'Krone', 'NOK', 'kr', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(78, 'Rials', 'OMR', '﷼', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(79, 'Rupees', 'PKR', '₨', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(80, 'Balboa', 'PAB', 'B/.', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(81, 'Guarani', 'PYG', 'Gs', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(82, 'Nuevos Soles', 'PEN', 'S/.', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(83, 'Pesos', 'PHP', 'Php', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(84, 'Zlotych', 'PLN', 'zł', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(85, 'Rials', 'QAR', '﷼', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(86, 'New Lei', 'RON', 'lei', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(87, 'Rubles', 'RUB', 'руб', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(88, 'Pounds', 'SHP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(89, 'Riyals', 'SAR', '﷼', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(90, 'Dinars', 'RSD', 'Дин.', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(91, 'Rupees', 'SCR', '₨', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(92, 'Dollars', 'SGD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(93, 'Dollars', 'SBD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(94, 'Shillings', 'SOS', 'S', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(95, 'Rand', 'ZAR', 'R', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(96, 'Rupees', 'LKR', '₨', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(97, 'Kronor', 'SEK', 'kr', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(98, 'Dollars', 'SRD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(99, 'Pounds', 'SYP', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(100, 'New Dollars', 'TWD', 'NT$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(101, 'Baht', 'THB', '฿', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(102, 'Dollars', 'TTD', 'TT$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(103, 'Lira', 'TRY', 'TL', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(104, 'Liras', 'TRL', '£', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(105, 'Dollars', 'TVD', '$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(106, 'Hryvnia', 'UAH', '₴', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(107, 'Pesos', 'UYU', '$U', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(108, 'Sums', 'UZS', 'лв', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(109, 'Bolivares Fuertes', 'VEF', 'Bs', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(110, 'Dong', 'VND', '₫', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(111, 'Rials', 'YER', '﷼', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(112, 'Taka', 'BDT', '৳', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(113, 'Zimbabwe Dollars', 'ZWD', 'Z$', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(114, 'Kenya', 'KES', 'KSh', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(115, 'Nigeria', 'naira', '₦', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(116, 'Ghana', 'GHS', 'GH₵', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(117, 'Ethiopian', 'ETB', 'Br', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(118, 'Tanzania', 'TZS', 'TSh', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(119, 'Uganda', 'UGX', 'USh', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(120, 'Rwandan', 'FRW', 'FRw', '2023-05-01 23:30:31', '2023-05-01 23:30:31');

-- --------------------------------------------------------

--
-- Table structure for table `date_formats`
--

CREATE TABLE `date_formats` (
  `id` bigint UNSIGNED NOT NULL,
  `format` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `normal_view` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `date_formats`
--

INSERT INTO `date_formats` (`id`, `format`, `normal_view`, `status`, `created_at`, `updated_at`) VALUES
(1, 'jS M, Y', '17th May, 2019', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(2, 'Y-m-d', '2019-05-17', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(3, 'Y-d-m', '2019-17-05', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(4, 'd-m-Y', '17-05-2019', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(5, 'm-d-Y', '05-17-2019', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(6, 'Y/m/d', '2019/05/17', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(7, 'Y/d/m', '2019/17/05', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(8, 'd/m/Y', '17/05/2019', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(9, 'm/d/Y', '05/17/2019', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(10, 'l jS \\of F Y', 'Monday 17th of May 2019', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(11, 'jS \\of F Y', '17th of May 2019', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(12, 'g:ia \\o\\n l jS F Y', '12:00am on Monday 17th May 2019', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(13, 'F j, Y, g:i a', 'May 7, 2019, 6:20 pm', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(14, 'F j, Y', 'May 17, 2019', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(15, '\\i\\t \\i\\s \\t\\h\\e jS \\d\\a\\y', 'it is the 17th day', 1, '2023-05-01 23:30:31', '2023-05-01 23:30:31');

-- --------------------------------------------------------

--
-- Table structure for table `designations`
--

CREATE TABLE `designations` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `designations`
--

INSERT INTO `designations` (`id`, `title`, `slug`, `created_at`, `updated_at`) VALUES
(1, 'HRM', 'hrm', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(2, 'Admin', 'admin', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(3, 'Accounts', 'accounts', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(4, 'Development', 'development', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(5, 'Software', 'software', '2023-05-01 23:30:31', '2023-05-01 23:30:31');

-- --------------------------------------------------------

--
-- Table structure for table `enrolls`
--

CREATE TABLE `enrolls` (
  `id` bigint UNSIGNED NOT NULL,
  `order_item_id` bigint UNSIGNED NOT NULL,
  `course_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `instructor_id` bigint UNSIGNED NOT NULL,
  `progress` int NOT NULL DEFAULT '0',
  `is_completed` tinyint(1) NOT NULL DEFAULT '0',
  `completed_lessons` json DEFAULT NULL,
  `completed_quizzes` json DEFAULT NULL,
  `completed_assignments` json DEFAULT NULL,
  `lesson_point` double(8,2) NOT NULL DEFAULT '0.00',
  `quiz_point` double(8,2) NOT NULL DEFAULT '0.00',
  `assignment_point` double(8,2) NOT NULL DEFAULT '0.00',
  `visited` timestamp NULL DEFAULT NULL,
  `completed_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

CREATE TABLE `expenses` (
  `id` bigint UNSIGNED NOT NULL,
  `transaction_id` bigint UNSIGNED NOT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '9',
  `amount` double(16,2) NOT NULL DEFAULT '0.00',
  `note` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `failed_jobs`
--

CREATE TABLE `failed_jobs` (
  `id` bigint UNSIGNED NOT NULL,
  `uuid` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `connection` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `queue` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `payload` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `exception` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `featured_courses`
--

CREATE TABLE `featured_courses` (
  `id` bigint UNSIGNED NOT NULL,
  `course_id` bigint UNSIGNED DEFAULT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `featured_courses`
--

INSERT INTO `featured_courses` (`id`, `course_id`, `status_id`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 2, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 3, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 4, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `flag_icons`
--

CREATE TABLE `flag_icons` (
  `id` bigint UNSIGNED NOT NULL,
  `icon_class` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `flag_icons`
--

INSERT INTO `flag_icons` (`id`, `icon_class`, `title`, `created_at`, `updated_at`) VALUES
(1, 'flag-icon flag-icon-ad', 'ad', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'flag-icon flag-icon-ae', 'ae', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'flag-icon flag-icon-af', 'af', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'flag-icon flag-icon-ag', 'ag', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(5, 'flag-icon flag-icon-ai', 'ai', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(6, 'flag-icon flag-icon-al', 'al', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(7, 'flag-icon flag-icon-am', 'am', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(8, 'flag-icon flag-icon-ao', 'ao', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(9, 'flag-icon flag-icon-aq', 'aq', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(10, 'flag-icon flag-icon-ar', 'ar', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(11, 'flag-icon flag-icon-as', 'as', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(12, 'flag-icon flag-icon-at', 'at', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(13, 'flag-icon flag-icon-au', 'au', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(14, 'flag-icon flag-icon-aw', 'aw', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(15, 'flag-icon flag-icon-ax', 'ax', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(16, 'flag-icon flag-icon-az', 'az', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(17, 'flag-icon flag-icon-ba', 'ba', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(18, 'flag-icon flag-icon-bb', 'bb', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(19, 'flag-icon flag-icon-bd', 'bd', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(20, 'flag-icon flag-icon-be', 'be', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(21, 'flag-icon flag-icon-bf', 'bf', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(22, 'flag-icon flag-icon-bg', 'bg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(23, 'flag-icon flag-icon-bh', 'bh', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(24, 'flag-icon flag-icon-bi', 'bi', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(25, 'flag-icon flag-icon-bj', 'bj', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(26, 'flag-icon flag-icon-bl', 'bl', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(27, 'flag-icon flag-icon-bm', 'bm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(28, 'flag-icon flag-icon-bn', 'bn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(29, 'flag-icon flag-icon-bo', 'bo', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(30, 'flag-icon flag-icon-bq', 'bq', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(31, 'flag-icon flag-icon-br', 'br', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(32, 'flag-icon flag-icon-bs', 'bs', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(33, 'flag-icon flag-icon-bt', 'bt', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(34, 'flag-icon flag-icon-bv', 'bv', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(35, 'flag-icon flag-icon-bw', 'bw', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(36, 'flag-icon flag-icon-by', 'by', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(37, 'flag-icon flag-icon-bz', 'bz', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(38, 'flag-icon flag-icon-ca', 'ca', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(39, 'flag-icon flag-icon-cc', 'cc', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(40, 'flag-icon flag-icon-cd', 'cd', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(41, 'flag-icon flag-icon-cf', 'cf', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(42, 'flag-icon flag-icon-cg', 'cg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(43, 'flag-icon flag-icon-ch', 'ch', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(44, 'flag-icon flag-icon-ci', 'ci', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(45, 'flag-icon flag-icon-ck', 'ck', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(46, 'flag-icon flag-icon-cl', 'cl', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(47, 'flag-icon flag-icon-cm', 'cm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(48, 'flag-icon flag-icon-cn', 'cn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(49, 'flag-icon flag-icon-co', 'co', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(50, 'flag-icon flag-icon-cr', 'cr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(51, 'flag-icon flag-icon-cu', 'cu', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(52, 'flag-icon flag-icon-cv', 'cv', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(53, 'flag-icon flag-icon-cw', 'cw', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(54, 'flag-icon flag-icon-cx', 'cx', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(55, 'flag-icon flag-icon-cy', 'cy', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(56, 'flag-icon flag-icon-cz', 'cz', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(57, 'flag-icon flag-icon-de', 'de', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(58, 'flag-icon flag-icon-dj', 'dj', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(59, 'flag-icon flag-icon-dk', 'dk', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(60, 'flag-icon flag-icon-dm', 'dm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(61, 'flag-icon flag-icon-do', 'do', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(62, 'flag-icon flag-icon-dz', 'dz', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(63, 'flag-icon flag-icon-ec', 'ec', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(64, 'flag-icon flag-icon-ee', 'ee', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(65, 'flag-icon flag-icon-eg', 'eg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(66, 'flag-icon flag-icon-eh', 'eh', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(67, 'flag-icon flag-icon-er', 'er', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(68, 'flag-icon flag-icon-es', 'es', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(69, 'flag-icon flag-icon-et', 'et', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(70, 'flag-icon flag-icon-fi', 'fi', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(71, 'flag-icon flag-icon-fj', 'fj', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(72, 'flag-icon flag-icon-fk', 'fk', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(73, 'flag-icon flag-icon-fm', 'fm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(74, 'flag-icon flag-icon-fo', 'fo', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(75, 'flag-icon flag-icon-fr', 'fr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(76, 'flag-icon flag-icon-ga', 'ga', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(77, 'flag-icon flag-icon-gb', 'gb', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(78, 'flag-icon flag-icon-gd', 'gd', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(79, 'flag-icon flag-icon-ge', 'ge', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(80, 'flag-icon flag-icon-gf', 'gf', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(81, 'flag-icon flag-icon-gg', 'gg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(82, 'flag-icon flag-icon-gh', 'gh', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(83, 'flag-icon flag-icon-gi', 'gi', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(84, 'flag-icon flag-icon-gl', 'gl', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(85, 'flag-icon flag-icon-gm', 'gm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(86, 'flag-icon flag-icon-gn', 'gn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(87, 'flag-icon flag-icon-gp', 'gp', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(88, 'flag-icon flag-icon-gq', 'gq', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(89, 'flag-icon flag-icon-gr', 'gr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(90, 'flag-icon flag-icon-gs', 'gs', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(91, 'flag-icon flag-icon-gt', 'gt', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(92, 'flag-icon flag-icon-gu', 'gu', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(93, 'flag-icon flag-icon-gw', 'gw', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(94, 'flag-icon flag-icon-gy', 'gy', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(95, 'flag-icon flag-icon-hk', 'hk', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(96, 'flag-icon flag-icon-hm', 'hm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(97, 'flag-icon flag-icon-hn', 'hn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(98, 'flag-icon flag-icon-hr', 'hr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(99, 'flag-icon flag-icon-ht', 'ht', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(100, 'flag-icon flag-icon-hu', 'hu', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(101, 'flag-icon flag-icon-id', 'id', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(102, 'flag-icon flag-icon-ie', 'ie', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(103, 'flag-icon flag-icon-il', 'il', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(104, 'flag-icon flag-icon-im', 'im', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(105, 'flag-icon flag-icon-in', 'in', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(106, 'flag-icon flag-icon-io', 'io', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(107, 'flag-icon flag-icon-iq', 'iq', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(108, 'flag-icon flag-icon-ir', 'ir', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(109, 'flag-icon flag-icon-is', 'is', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(110, 'flag-icon flag-icon-it', 'it', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(111, 'flag-icon flag-icon-je', 'je', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(112, 'flag-icon flag-icon-jm', 'jm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(113, 'flag-icon flag-icon-jo', 'jo', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(114, 'flag-icon flag-icon-jp', 'jp', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(115, 'flag-icon flag-icon-ke', 'ke', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(116, 'flag-icon flag-icon-kg', 'kg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(117, 'flag-icon flag-icon-kh', 'kh', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(118, 'flag-icon flag-icon-ki', 'ki', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(119, 'flag-icon flag-icon-km', 'km', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(120, 'flag-icon flag-icon-kn', 'kn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(121, 'flag-icon flag-icon-kp', 'kp', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(122, 'flag-icon flag-icon-kr', 'kr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(123, 'flag-icon flag-icon-kw', 'kw', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(124, 'flag-icon flag-icon-ky', 'ky', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(125, 'flag-icon flag-icon-kz', 'kz', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(126, 'flag-icon flag-icon-la', 'la', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(127, 'flag-icon flag-icon-lb', 'lb', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(128, 'flag-icon flag-icon-lc', 'lc', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(129, 'flag-icon flag-icon-li', 'li', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(130, 'flag-icon flag-icon-lk', 'lk', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(131, 'flag-icon flag-icon-lr', 'lr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(132, 'flag-icon flag-icon-ls', 'ls', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(133, 'flag-icon flag-icon-lt', 'lt', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(134, 'flag-icon flag-icon-lu', 'lu', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(135, 'flag-icon flag-icon-lv', 'lv', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(136, 'flag-icon flag-icon-ly', 'ly', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(137, 'flag-icon flag-icon-ma', 'ma', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(138, 'flag-icon flag-icon-mc', 'mc', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(139, 'flag-icon flag-icon-md', 'md', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(140, 'flag-icon flag-icon-me', 'me', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(141, 'flag-icon flag-icon-mf', 'mf', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(142, 'flag-icon flag-icon-mg', 'mg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(143, 'flag-icon flag-icon-mh', 'mh', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(144, 'flag-icon flag-icon-mk', 'mk', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(145, 'flag-icon flag-icon-ml', 'ml', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(146, 'flag-icon flag-icon-mm', 'mm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(147, 'flag-icon flag-icon-mn', 'mn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(148, 'flag-icon flag-icon-mo', 'mo', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(149, 'flag-icon flag-icon-mp', 'mp', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(150, 'flag-icon flag-icon-mq', 'mq', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(151, 'flag-icon flag-icon-mr', 'mr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(152, 'flag-icon flag-icon-ms', 'ms', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(153, 'flag-icon flag-icon-mt', 'mt', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(154, 'flag-icon flag-icon-mu', 'mu', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(155, 'flag-icon flag-icon-mv', 'mv', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(156, 'flag-icon flag-icon-mw', 'mw', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(157, 'flag-icon flag-icon-mx', 'mx', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(158, 'flag-icon flag-icon-my', 'my', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(159, 'flag-icon flag-icon-mz', 'mz', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(160, 'flag-icon flag-icon-na', 'na', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(161, 'flag-icon flag-icon-nc', 'nc', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(162, 'flag-icon flag-icon-ne', 'ne', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(163, 'flag-icon flag-icon-nf', 'nf', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(164, 'flag-icon flag-icon-ng', 'ng', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(165, 'flag-icon flag-icon-ni', 'ni', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(166, 'flag-icon flag-icon-nl', 'nl', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(167, 'flag-icon flag-icon-no', 'no', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(168, 'flag-icon flag-icon-np', 'np', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(169, 'flag-icon flag-icon-nr', 'nr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(170, 'flag-icon flag-icon-nu', 'nu', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(171, 'flag-icon flag-icon-nz', 'nz', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(172, 'flag-icon flag-icon-om', 'om', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(173, 'flag-icon flag-icon-pa', 'pa', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(174, 'flag-icon flag-icon-pe', 'pe', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(175, 'flag-icon flag-icon-pf', 'pf', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(176, 'flag-icon flag-icon-pg', 'pg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(177, 'flag-icon flag-icon-ph', 'ph', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(178, 'flag-icon flag-icon-pk', 'pk', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(179, 'flag-icon flag-icon-pl', 'pl', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(180, 'flag-icon flag-icon-pm', 'pm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(181, 'flag-icon flag-icon-pn', 'pn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(182, 'flag-icon flag-icon-pr', 'pr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(183, 'flag-icon flag-icon-ps', 'ps', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(184, 'flag-icon flag-icon-pt', 'pt', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(185, 'flag-icon flag-icon-pw', 'pw', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(186, 'flag-icon flag-icon-py', 'py', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(187, 'flag-icon flag-icon-qa', 'qa', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(188, 'flag-icon flag-icon-re', 're', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(189, 'flag-icon flag-icon-ro', 'ro', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(190, 'flag-icon flag-icon-rs', 'rs', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(191, 'flag-icon flag-icon-ru', 'ru', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(192, 'flag-icon flag-icon-rw', 'rw', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(193, 'flag-icon flag-icon-sa', 'sa', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(194, 'flag-icon flag-icon-sb', 'sb', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(195, 'flag-icon flag-icon-sc', 'sc', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(196, 'flag-icon flag-icon-sd', 'sd', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(197, 'flag-icon flag-icon-se', 'se', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(198, 'flag-icon flag-icon-sg', 'sg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(199, 'flag-icon flag-icon-sh', 'sh', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(200, 'flag-icon flag-icon-si', 'si', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(201, 'flag-icon flag-icon-sj', 'sj', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(202, 'flag-icon flag-icon-sk', 'sk', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(203, 'flag-icon flag-icon-sl', 'sl', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(204, 'flag-icon flag-icon-sm', 'sm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(205, 'flag-icon flag-icon-sn', 'sn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(206, 'flag-icon flag-icon-so', 'so', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(207, 'flag-icon flag-icon-sr', 'sr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(208, 'flag-icon flag-icon-ss', 'ss', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(209, 'flag-icon flag-icon-st', 'st', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(210, 'flag-icon flag-icon-sv', 'sv', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(211, 'flag-icon flag-icon-sx', 'sx', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(212, 'flag-icon flag-icon-sy', 'sy', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(213, 'flag-icon flag-icon-sz', 'sz', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(214, 'flag-icon flag-icon-tc', 'tc', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(215, 'flag-icon flag-icon-td', 'td', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(216, 'flag-icon flag-icon-tf', 'tf', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(217, 'flag-icon flag-icon-tg', 'tg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(218, 'flag-icon flag-icon-th', 'th', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(219, 'flag-icon flag-icon-tj', 'tj', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(220, 'flag-icon flag-icon-tk', 'tk', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(221, 'flag-icon flag-icon-tl', 'tl', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(222, 'flag-icon flag-icon-tm', 'tm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(223, 'flag-icon flag-icon-tn', 'tn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(224, 'flag-icon flag-icon-to', 'to', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(225, 'flag-icon flag-icon-tr', 'tr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(226, 'flag-icon flag-icon-tt', 'tt', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(227, 'flag-icon flag-icon-tv', 'tv', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(228, 'flag-icon flag-icon-tw', 'tw', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(229, 'flag-icon flag-icon-tz', 'tz', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(230, 'flag-icon flag-icon-ua', 'ua', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(231, 'flag-icon flag-icon-ug', 'ug', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(232, 'flag-icon flag-icon-um', 'um', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(233, 'flag-icon flag-icon-us', 'us', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(234, 'flag-icon flag-icon-uy', 'uy', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(235, 'flag-icon flag-icon-uz', 'uz', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(236, 'flag-icon flag-icon-va', 'va', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(237, 'flag-icon flag-icon-vc', 'vc', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(238, 'flag-icon flag-icon-ve', 've', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(239, 'flag-icon flag-icon-vg', 'vg', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(240, 'flag-icon flag-icon-vi', 'vi', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(241, 'flag-icon flag-icon-vn', 'vn', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(242, 'flag-icon flag-icon-vu', 'vu', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(243, 'flag-icon flag-icon-wf', 'wf', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(244, 'flag-icon flag-icon-ws', 'ws', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(245, 'flag-icon flag-icon-ye', 'ye', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(246, 'flag-icon flag-icon-yt', 'yt', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(247, 'flag-icon flag-icon-za', 'za', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(248, 'flag-icon flag-icon-zm', 'zm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(249, 'flag-icon flag-icon-zw', 'zw', '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `footer_menus`
--

CREATE TABLE `footer_menus` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `column` int NOT NULL DEFAULT '1' COMMENT '1=column 1, 2=column 2, 3=column 3',
  `links` json DEFAULT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `footer_menus`
--

INSERT INTO `footer_menus` (`id`, `name`, `column`, `links`, `status_id`, `created_at`, `updated_at`) VALUES
(1, 'Pages', 1, '[{\"link\": \"http://o-academy.test/courses?sort=latest\", \"name\": \"Latest Courses\", \"status_id\": 1}, {\"link\": \"http://o-academy.test/courses?sort=popular\", \"name\": \"Most Popular Courses\", \"status_id\": 1}, {\"link\": \"http://o-academy.test/courses?sort=best_rated\", \"name\": \"Best Rated Courses\", \"status_id\": 1}, {\"link\": \"http://o-academy.test/blogs\", \"name\": \"Our Recent Blogs\", \"status_id\": 1}]', 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Custom Links', 2, '[{\"name\": \"About Us\", \"is_page\": \"1\", \"page_id\": \"3\", \"status_id\": 1}, {\"link\": \"http://o-academy.test/contact/us\", \"name\": \"Contact Us\", \"status_id\": 1}, {\"link\": \"http://o-academy.test/privacy-policy\", \"name\": \"Privacy Policy\", \"is_page\": \"1\", \"page_id\": \"1\", \"status_id\": 1}, {\"link\": \"http://o-academy.test/terms-conditions\", \"name\": \"Terms & Conditions\", \"is_page\": \"1\", \"page_id\": \"2\", \"status_id\": 1}]', 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'Top Categories', 3, '[{\"link\": \"http://o-academy.test/category?q=web-development\", \"name\": \"Web Development\", \"status_id\": 1}, {\"link\": \"http://o-academy.test/category?q=mobile-development\", \"name\": \"Mobile Development\", \"status_id\": 1}, {\"link\": \"http://o-academy.test/category?q=game-development\", \"name\": \"Game Development\", \"status_id\": 1}, {\"link\": \"http://o-academy.test/category?q=seo\", \"name\": \"Seo\", \"status_id\": 1}]', 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `incomes`
--

CREATE TABLE `incomes` (
  `id` bigint UNSIGNED NOT NULL,
  `transaction_id` bigint UNSIGNED NOT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '9',
  `amount` double(16,2) NOT NULL DEFAULT '0.00',
  `note` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `instructors`
--

CREATE TABLE `instructors` (
  `id` bigint UNSIGNED NOT NULL,
  `about_me` longtext COLLATE utf8mb4_unicode_ci,
  `designation` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` tinyint NOT NULL DEFAULT '1' COMMENT '1 = male',
  `date_of_birth` date DEFAULT NULL,
  `badges` json DEFAULT NULL,
  `education` json DEFAULT NULL,
  `experience` json DEFAULT NULL,
  `skills` json DEFAULT NULL,
  `commission` double NOT NULL DEFAULT '20',
  `earnings` double NOT NULL DEFAULT '0',
  `balance` double NOT NULL DEFAULT '0',
  `points` double NOT NULL DEFAULT '0',
  `country_id` bigint UNSIGNED DEFAULT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `instructors`
--

INSERT INTO `instructors` (`id`, `about_me`, `designation`, `address`, `gender`, `date_of_birth`, `badges`, `education`, `experience`, `skills`, `commission`, `earnings`, `balance`, `points`, `country_id`, `user_id`, `created_at`, `updated_at`) VALUES
(1, 'Lorem Ipsum Is Simply Dummy Text Of The Printing And Typesetting Industry. Lorem Ipsum Has Been The Industry\'s Standard Dummy Text Ever Since The 1500s, When An Unknown Printer Took A Galley Of Type And Scrambled It To Make A Type Specimen Book. It Has Survived Not Only Five Centuries, But Also The Leap Into Electronic Typesetting, Remaining Essentially Unchanged.\n\n                It Was Popularised In The 1960s With The Release Of Letraset Sheets Containing Lorem Ipsum Passages, And More Recently With Desktop Publishing Software Like Aldus PageMaker Including Versions Of Lorem Ipsum.', 'Software engineer | Laravel | PHP', 'Dhaka, Bangladesh', 1, NULL, NULL, '[{\"name\": \"Lorem Ipsum is simply dummy text of the printing\", \"degree\": \"Lorem Ipsum\", \"current\": 0, \"program\": \"Lorem Ipsum\", \"end_date\": \"03/28/2018\", \"start_date\": \"03/01/2014\", \"description\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\"}]', '[{\"name\": \"Maya Lucas\", \"title\": \"Senior Software Engineer\", \"current\": 1, \"end_date\": null, \"location\": \"Deserunt rerum volup\", \"start_date\": \"03/28/2023\", \"description\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"employee_type\": \"full_time\", \"location_type\": \"hybrid\"}]', '[{\"value\": \"Nodejs\"}, {\"value\": \"laravel\"}, {\"value\": \"php\"}, {\"value\": \"javascript\"}, {\"value\": \"css\"}, {\"value\": \"html\"}, {\"value\": \"vue.js\"}, {\"value\": \"react.js\"}]', 20, 0, 0, 0, 19, 5, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Lorem Ipsum Is Simply Dummy Text Of The Printing And Typesetting Industry. Lorem Ipsum Has Been The Industry\'s Standard Dummy Text Ever Since The 1500s, When An Unknown Printer Took A Galley Of Type And Scrambled It To Make A Type Specimen Book. It Has Survived Not Only Five Centuries, But Also The Leap Into Electronic Typesetting, Remaining Essentially Unchanged.\n\n                    It Was Popularised In The 1960s With The Release Of Letraset Sheets Containing Lorem Ipsum Passages, And More Recently With Desktop Publishing Software Like Aldus PageMaker Including Versions Of Lorem Ipsum.', 'Software engineer | Laravel | PHP', 'Dhaka, Bangladesh', 1, NULL, NULL, '[{\"name\": \"Lorem Ipsum is simply dummy text of the printing\", \"degree\": \"Lorem Ipsum\", \"current\": 0, \"program\": \"Lorem Ipsum\", \"end_date\": \"03/28/2018\", \"start_date\": \"03/01/2014\", \"description\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\"}]', '[{\"name\": \"Maya Lucas\", \"title\": \"Senior Software Engineer\", \"current\": 1, \"end_date\": null, \"location\": \"Deserunt rerum volup\", \"start_date\": \"03/28/2023\", \"description\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"employee_type\": \"full_time\", \"location_type\": \"hybrid\"}]', '[{\"value\": \"Nodejs\"}, {\"value\": \"laravel\"}, {\"value\": \"php\"}, {\"value\": \"javascript\"}, {\"value\": \"css\"}, {\"value\": \"html\"}, {\"value\": \"vue.js\"}, {\"value\": \"react.js\"}]', 20, 0, 0, 0, 19, 7, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `instructor_payment_methods`
--

CREATE TABLE `instructor_payment_methods` (
  `id` bigint UNSIGNED NOT NULL,
  `payment_method_id` bigint UNSIGNED NOT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `credentials` json DEFAULT NULL,
  `is_default` tinyint NOT NULL DEFAULT '0' COMMENT '1 = default',
  `user_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` bigint UNSIGNED NOT NULL,
  `queue` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payload` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `attempts` tinyint UNSIGNED NOT NULL,
  `reserved_at` int UNSIGNED DEFAULT NULL,
  `available_at` int UNSIGNED NOT NULL,
  `created_at` int UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `languages`
--

CREATE TABLE `languages` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `icon_class` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direction` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `languages`
--

INSERT INTO `languages` (`id`, `name`, `code`, `icon_class`, `direction`, `created_at`, `updated_at`) VALUES
(1, 'English', 'en', 'flag-icon flag-icon-us', 'ltr', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Bangla', 'bn', 'flag-icon flag-icon-bd', 'ltr', '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `lessons`
--

CREATE TABLE `lessons` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_quiz` tinyint NOT NULL DEFAULT '0' COMMENT '0 = false, 1 = true',
  `is_timer` tinyint NOT NULL DEFAULT '0' COMMENT '0 = false, 1 = true',
  `duration` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `point` double(8,2) NOT NULL DEFAULT '0.00',
  `section_id` bigint UNSIGNED DEFAULT NULL,
  `course_id` bigint UNSIGNED DEFAULT NULL,
  `is_free` tinyint NOT NULL DEFAULT '0' COMMENT '0 = false, 1 = true',
  `lesson_type` enum('Youtube','Vimeo','VideoFile','GoogleDrive','DocumentFile','Text','ImageFile','IframeEmbed') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `video_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `video_type` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `video_file` bigint UNSIGNED DEFAULT NULL,
  `attachment_type` tinyint NOT NULL DEFAULT '0' COMMENT '0 = file, 1 = link',
  `attachment` bigint UNSIGNED DEFAULT NULL,
  `image_file` bigint UNSIGNED DEFAULT NULL,
  `is_online_view` tinyint NOT NULL DEFAULT '0' COMMENT '0 = false, 1 = true',
  `is_downloadable` tinyint NOT NULL DEFAULT '0' COMMENT '0 = false, 1 = true',
  `iframe` longtext COLLATE utf8mb4_unicode_ci,
  `lesson_text` longtext COLLATE utf8mb4_unicode_ci,
  `content` longtext COLLATE utf8mb4_unicode_ci,
  `order` int NOT NULL DEFAULT '1',
  `marks` int NOT NULL DEFAULT '0',
  `pass_marks` int NOT NULL DEFAULT '0',
  `instruction` longtext COLLATE utf8mb4_unicode_ci,
  `last_modified` timestamp NULL DEFAULT NULL,
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '21',
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `lessons`
--

INSERT INTO `lessons` (`id`, `title`, `is_quiz`, `is_timer`, `duration`, `point`, `section_id`, `course_id`, `is_free`, `lesson_type`, `video_url`, `video_type`, `video_file`, `attachment_type`, `attachment`, `image_file`, `is_online_view`, `is_downloadable`, `iframe`, `lesson_text`, `content`, `order`, `marks`, `pass_marks`, `instruction`, `last_modified`, `created_by`, `updated_by`, `status_id`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Lesson 1', 0, 0, '120', 50.00, 1, 1, 0, 'Youtube', 'https://youtu.be/3l6Q4QL-j4Q', NULL, NULL, 0, NULL, NULL, 0, 0, NULL, 'This is lesson text', 'Lesson 1', 1, 0, 0, NULL, NULL, 5, 1, 21, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Quiz 1', 1, 0, '60', 100.00, 1, 1, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, NULL, NULL, NULL, 1, 100, 40, 'Quiz 1', NULL, 5, 1, 21, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'Lesson 2', 0, 0, '160', 50.00, 2, 1, 0, 'Vimeo', 'https://vimeo.com/24456787', NULL, NULL, 0, NULL, NULL, 0, 0, NULL, NULL, 'Lesson 2', 2, 0, 0, NULL, NULL, 5, 1, 21, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'Lesson 3', 0, 0, '40', 50.00, 3, 1, 0, 'Text', NULL, NULL, NULL, 0, NULL, NULL, 0, 0, NULL, 'This is lesson text', 'Lesson 3', 3, 0, 0, NULL, NULL, 5, 1, 21, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(5, 'Lesson 4', 0, 0, '220', 50.00, 4, 1, 0, 'Text', NULL, NULL, NULL, 0, NULL, NULL, 0, 0, NULL, 'This is lesson text', 'Lesson 4', 4, 0, 0, NULL, NULL, 5, 1, 21, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int UNSIGNED NOT NULL,
  `migration` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `batch` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '2013_01_31_091321_create_uploads_table', 1),
(2, '2013_08_03_072003_create_roles_table', 1),
(3, '2013_08_17_074050_create_statuses_table', 1),
(4, '2014_10_12_000000_create_users_table', 1),
(5, '2014_10_12_100000_create_password_resets_table', 1),
(6, '2019_08_19_000000_create_failed_jobs_table', 1),
(7, '2019_12_14_000001_create_personal_access_tokens_table', 1),
(8, '2022_07_19_045514_create_flag_icons_table', 1),
(9, '2022_08_08_043550_create_permissions_table', 1),
(10, '2022_08_17_092623_create_languages_table', 1),
(11, '2022_10_04_044255_create_searches_table', 1),
(12, '2022_10_13_064230_create_designations_table', 1),
(13, '2023_01_30_094132_create_course_categories_table', 1),
(14, '2023_01_31_052613_create_courses_table', 1),
(15, '2023_01_31_071132_create_sections_table', 1),
(16, '2023_01_31_073632_create_lessons_table', 1),
(17, '2023_01_31_102629_create_questions_table', 1),
(18, '2023_01_31_114255_create_notice_boards_table', 1),
(19, '2023_01_31_114712_create_assignments_table', 1),
(20, '2023_02_04_090153_create_blog_categories_table', 1),
(21, '2023_02_05_064849_create_blogs_table', 1),
(22, '2023_02_09_062808_create_sliders_table', 1),
(23, '2023_02_10_092900_create_pages_table', 1),
(24, '2023_02_13_095025_create_brands_table', 1),
(25, '2023_02_16_054800_create_countries_table', 1),
(26, '2023_02_18_054704_create_instructors_table', 1),
(27, '2023_02_20_041130_create_carts_table', 1),
(28, '2023_02_22_035228_create_payment_methods_table', 1),
(29, '2023_02_22_040205_create_orders_table', 1),
(30, '2023_02_22_040220_create_order_items_table', 1),
(31, '2023_02_22_123341_create_enrolls_table', 1),
(32, '2023_02_22_132758_create_jobs_table', 1),
(33, '2023_02_23_055405_create_assignment_submits_table', 1),
(34, '2023_02_23_102707_create_quiz_results_table', 1),
(35, '2023_02_25_054301_create_reviews_table', 1),
(36, '2023_02_25_100524_create_notes_table', 1),
(37, '2023_02_27_132850_create_question_submits_table', 1),
(38, '2023_03_01_080253_create_bookmarks_table', 1),
(39, '2023_03_01_102004_create_students_table', 1),
(40, '2023_03_09_051502_create_featured_courses_table', 1),
(41, '2023_03_09_051834_create_settings_table', 1),
(42, '2023_03_10_051127_create_app_home_sections_table', 1),
(43, '2023_03_13_040838_create_instructor_payment_methods_table', 1),
(44, '2023_03_13_054814_create_payouts_table', 1),
(45, '2023_03_13_055026_create_payments_table', 1),
(46, '2023_03_16_084756_create_certificate_templates_table', 1),
(47, '2023_03_16_084803_create_certificate_generates_table', 1),
(48, '2023_03_27_085756_create_footer_menus_table', 1),
(49, '2023_04_04_084513_create_testimonials_table', 1),
(50, '2023_04_05_062621_create_accounts_table', 1),
(51, '2023_04_05_062641_create_transactions_table', 1),
(52, '2023_04_05_062835_create_incomes_table', 1),
(53, '2023_04_05_062857_create_expenses_table', 1),
(54, '2023_04_06_021209_create_payout_logs_table', 1),
(55, '2023_04_10_085742_create_currencies_table', 1),
(56, '2023_04_10_090342_create_date_formats_table', 1),
(57, '2023_04_27_091637_create_contacts_table', 1);

-- --------------------------------------------------------

--
-- Table structure for table `notes`
--

CREATE TABLE `notes` (
  `id` bigint UNSIGNED NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `enroll_id` bigint UNSIGNED NOT NULL,
  `lesson_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notice_boards`
--

CREATE TABLE `notice_boards` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `course_id` bigint UNSIGNED DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `is_send_mail` bigint UNSIGNED NOT NULL DEFAULT '0' COMMENT '0 = No, 1 = Yes',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `notice_boards`
--

INSERT INTO `notice_boards` (`id`, `title`, `course_id`, `description`, `is_send_mail`, `status_id`, `created_by`, `updated_by`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Noticeboard 1', 1, 'Noticeboard 1', 0, 1, 5, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Noticeboard 2', 1, 'Noticeboard 2', 0, 1, 5, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'Noticeboard 3', 1, 'Noticeboard 3', 0, 1, 5, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'Noticeboard 4', 1, 'Noticeboard 4', 0, 1, 5, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `payment_method` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payment_details` text COLLATE utf8mb4_unicode_ci,
  `invoice_number` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `amount` double(8,2) NOT NULL,
  `discount_amount` double(8,2) DEFAULT NULL,
  `total_amount` double(8,2) NOT NULL,
  `paid_amount` double(8,2) DEFAULT NULL,
  `due_amount` double(8,2) DEFAULT NULL,
  `tax_amount` double(8,2) DEFAULT NULL,
  `status` enum('unpaid','processing','paid','failed') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'unpaid',
  `is_refunded` tinyint NOT NULL DEFAULT '0',
  `reference_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` bigint UNSIGNED NOT NULL,
  `order_id` bigint UNSIGNED NOT NULL,
  `course_id` bigint UNSIGNED NOT NULL,
  `amount` double(8,2) NOT NULL,
  `discount_amount` double(8,2) DEFAULT NULL,
  `total_amount` double(8,2) NOT NULL DEFAULT '0.00',
  `tax_amount` double(8,2) NOT NULL DEFAULT '0.00',
  `commission_amount` double(8,2) NOT NULL DEFAULT '0.00',
  `instructor_amount` double(8,2) NOT NULL DEFAULT '0.00',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pages`
--

CREATE TABLE `pages` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_by` bigint UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `pages`
--

INSERT INTO `pages` (`id`, `title`, `slug`, `content`, `status_id`, `created_by`, `updated_by`, `deleted_by`, `created_at`, `updated_at`) VALUES
(1, 'Privacy Policy', 'privacy-policy', '<p>We at Wasai LLC respect the privacy of your personal information and, as such, make every effort to ensure your information is protected and remains private. As the owner and operator of loremipsum.io (the \"Website\") hereafter referred to in this Privacy Policy as \"Lorem Ipsum\", \"us\", \"our\" or \"we\", we have provided this Privacy Policy to explain how we collect, use, share and protect information about the users of our Website (hereafter referred to as “user”, “you” or \"your\"). For the purposes of this Agreement, any use of the terms \"Lorem Ipsum\", \"us\", \"our\" or \"we\" includes Wasai LLC, without limitation. We will not use or share your personal information with anyone except as described in this Privacy Policy.</p><p>This Privacy Policy will inform you about the types of personal data we collect, the purposes for which we use the data, the ways in which the data is handled and your rights with regard to your personal data. Furthermore, this Privacy Policy is intended to satisfy the obligation of transparency under the EU General Data Protection Regulation 2016/679 (\"GDPR\") and the laws implementing GDPR.</p><p>For the purpose of this Privacy Policy the Data Controller of personal data is Wasai LLC and our contact details are set out in the Contact section at the end of this Privacy Policy. Data Controller means the natural or legal person who (either alone or jointly or in common with other persons) determines the purposes for which and the manner in which any personal information are, or are to be, processed.</p><p>For purposes of this Privacy Policy, \"Your Information\" or \"Personal Data\" means information about you, which may be of a confidential or sensitive nature and may include personally identifiable information (\"PII\") and/or financial information. PII means individually identifiable information that would allow us to determine the actual identity of a specific living person, while sensitive data may include information, comments, content and other information that you voluntarily provide.</p><p>Lorem Ipsum collects information about you when you use our Website to access our services, and other online products and services (collectively, the “Services”) and through other interactions and communications you have with us. The term Services includes, collectively, various applications, websites, widgets, email notifications and other mediums, or portions of such mediums, through which you have accessed this Privacy Policy.</p><p>We may change this Privacy Policy from time to time. If we decide to change this Privacy Policy, we will inform you by posting the revised Privacy Policy on the Site. Those changes will go into effect on the \"Last updated\" date shown at the end of this Privacy Policy. By continuing to use the Site or Services, you consent to the revised Privacy Policy. We encourage you to periodically review the Privacy Policy for the latest information on our privacy practices.</p><p>BY ACCESSING OR USING OUR SERVICES, YOU CONSENT TO THE COLLECTION, TRANSFER, MANIPULATION, STORAGE, DISCLOSURE AND OTHER USES OF YOUR INFORMATION (COLLECTIVELY, \"USE OF YOUR INFORMATION\") AS DESCRIBED IN THIS PRIVACY POLICY. IF YOU DO NOT AGREE WITH OR CONSENT TO THIS PRIVACY POLICY YOU MAY NOT ACCESS OR USE OUR SERVICES.</p>', 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Terms And Condition', 'terms-and-condition', '<p>We at Wasai LLC respect the privacy of your personal information and, as such, make every effort to ensure your information is protected and remains private. As the owner and operator of loremipsum.io (the \"Website\") hereafter referred to in this Privacy Policy as \"Lorem Ipsum\", \"us\", \"our\" or \"we\", we have provided this Privacy Policy to explain how we collect, use, share and protect information about the users of our Website (hereafter referred to as “user”, “you” or \"your\"). For the purposes of this Agreement, any use of the terms \"Lorem Ipsum\", \"us\", \"our\" or \"we\" includes Wasai LLC, without limitation. We will not use or share your personal information with anyone except as described in this Privacy Policy.</p><p>This Privacy Policy will inform you about the types of personal data we collect, the purposes for which we use the data, the ways in which the data is handled and your rights with regard to your personal data. Furthermore, this Privacy Policy is intended to satisfy the obligation of transparency under the EU General Data Protection Regulation 2016/679 (\"GDPR\") and the laws implementing GDPR.</p><p>For the purpose of this Privacy Policy the Data Controller of personal data is Wasai LLC and our contact details are set out in the Contact section at the end of this Privacy Policy. Data Controller means the natural or legal person who (either alone or jointly or in common with other persons) determines the purposes for which and the manner in which any personal information are, or are to be, processed.</p><p>For purposes of this Privacy Policy, \"Your Information\" or \"Personal Data\" means information about you, which may be of a confidential or sensitive nature and may include personally identifiable information (\"PII\") and/or financial information. PII means individually identifiable information that would allow us to determine the actual identity of a specific living person, while sensitive data may include information, comments, content and other information that you voluntarily provide.</p><p>Lorem Ipsum collects information about you when you use our Website to access our services, and other online products and services (collectively, the “Services”) and through other interactions and communications you have with us. The term Services includes, collectively, various applications, websites, widgets, email notifications and other mediums, or portions of such mediums, through which you have accessed this Privacy Policy.</p><p>We may change this Privacy Policy from time to time. If we decide to change this Privacy Policy, we will inform you by posting the revised Privacy Policy on the Site. Those changes will go into effect on the \"Last updated\" date shown at the end of this Privacy Policy. By continuing to use the Site or Services, you consent to the revised Privacy Policy. We encourage you to periodically review the Privacy Policy for the latest information on our privacy practices.</p><p>BY ACCESSING OR USING OUR SERVICES, YOU CONSENT TO THE COLLECTION, TRANSFER, MANIPULATION, STORAGE, DISCLOSURE AND OTHER USES OF YOUR INFORMATION (COLLECTIVELY, \"USE OF YOUR INFORMATION\") AS DESCRIBED IN THIS PRIVACY POLICY. IF YOU DO NOT AGREE WITH OR CONSENT TO THIS PRIVACY POLICY YOU MAY NOT ACCESS OR USE OUR SERVICES.</p>', 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'About Us', 'about-us', '<p>Welcome to our About Us page!</p><p>We are a team of dedicated professionals who are passionate about using technology to create innovative solutions that make a difference in people\'s lives. Our company was founded with the vision of providing exceptional service to our customers, and we strive to exceed their expectations every day.</p><p>Our mission is to empower businesses and individuals with the tools they need to succeed in a rapidly evolving digital landscape. We understand the challenges of navigating the ever-changing technology landscape, and we are committed to helping our clients stay ahead of the curve.</p><p>Our team is comprised of experts in a wide range of fields, including software development, data analysis, design, and marketing. We work collaboratively to deliver exceptional results, and we are committed to providing our clients with the highest level of customer service.</p><p>At our core, we believe that technology should be used to make people\'s lives easier and more productive. That\'s why we are dedicated to creating solutions that are intuitive, user-friendly, and effective.</p><p>Thank you for taking the time to learn more about us. We look forward to working with you to achieve your goals!</p>', 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `password_resets`
--

CREATE TABLE `password_resets` (
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `payout_id` bigint UNSIGNED NOT NULL,
  `amount` double(8,2) NOT NULL,
  `status` enum('unpaid','processing','paid','failed') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'unpaid',
  `payment_details` text COLLATE utf8mb4_unicode_ci,
  `invoice_number` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payment_methods`
--

CREATE TABLE `payment_methods` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_id` bigint UNSIGNED DEFAULT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `credentials` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `payment_methods`
--

INSERT INTO `payment_methods` (`id`, `title`, `name`, `image_id`, `status_id`, `credentials`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'Stripe', 'stripe', NULL, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32', NULL),
(2, 'Sslcommerz', 'sslcommerz', NULL, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `payouts`
--

CREATE TABLE `payouts` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `instructor_payment_method_id` bigint UNSIGNED NOT NULL,
  `amount` double(8,2) NOT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '3',
  `payment_status_id` bigint UNSIGNED NOT NULL DEFAULT '9',
  `payment_details` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payout_logs`
--

CREATE TABLE `payout_logs` (
  `id` bigint UNSIGNED NOT NULL,
  `payout_id` bigint UNSIGNED NOT NULL,
  `status_id` bigint UNSIGNED NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `user_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE `permissions` (
  `id` bigint UNSIGNED NOT NULL,
  `attribute` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `keywords` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `permissions`
--

INSERT INTO `permissions` (`id`, `attribute`, `keywords`, `created_at`, `updated_at`) VALUES
(1, 'users', '{\"read\":\"user_read\",\"create\":\"user_create\",\"update\":\"user_update\",\"delete\":\"user_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'roles', '{\"read\":\"role_read\",\"create\":\"role_create\",\"update\":\"role_update\",\"delete\":\"role_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'language', '{\"read\":\"language_read\",\"create\":\"language_create\",\"update\":\"language_update\",\"update terms\":\"language_update_terms\",\"delete\":\"language_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'ai_support', '{\"ai_support\":\"ai_support\",\"ai_support_find\":\"ai_support_find\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(5, 'course_category', '{\"read\":\"course_category_read\",\"create\":\"course_category_create\",\"store\":\"course_category_store\",\"update\":\"course_category_update\",\"delete\":\"course_category_delete\",\"popular_course_category_list\":\"popular_course_category_list\",\"popular_course_category_added\":\"popular_course_category_added\",\"popular_course_category_deleted\":\"popular_course_category_deleted\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(6, 'course', '{\"read\":\"course_read\",\"create\":\"course_create\",\"store\":\"course_store\",\"update\":\"course_update\",\"delete\":\"course_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(7, 'course_assignment', '{\"assignment_list\":\"course_assignment_list\",\"assignment_create\":\"course_assignment_create\",\"assignment_store\":\"course_assignment_store\",\"assignment_update\":\"course_assignment_update\",\"assignment_delete\":\"course_assignment_delete\",\"assignment_submission_list\":\"course_assignment_submission_list\",\"assignment_submission_view\":\"course_assignment_submission_view\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(8, 'course_noticeboard', '{\"noticeboard_list\":\"course_noticeboard_list\",\"noticeboard_create\":\"course_noticeboard_create\",\"noticeboard_store\":\"course_noticeboard_store\",\"noticeboard_update\":\"course_noticeboard_update\",\"noticeboard_delete\":\"course_noticeboard_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(9, 'course_curriculum', '{\"course_curriculum\":\"course_curriculum\",\"course_curriculum_create\":\"course_curriculum_create\",\"course_curriculum_store\":\"course_curriculum_store\",\"course_curriculum_update\":\"course_curriculum_update\",\"course_curriculum_delete\":\"course_curriculum_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(10, 'course_lesson', '{\"course_lesson\":\"course_lesson\",\"course_lesson_create\":\"course_lesson_create\",\"course_lesson_store\":\"course_lesson_store\",\"course_lesson_update\":\"course_lesson_update\",\"course_lesson_delete\":\"course_lesson_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(11, 'course_quiz', '{\"course_quiz\":\"course_quiz_list\",\"course_quiz_create\":\"course_quiz_create\",\"course_quiz_store\":\"course_quiz_store\",\"course_quiz_update\":\"course_quiz_update\",\"course_quiz_delete\":\"course_quiz_delete\",\"quiz_submission_list\":\"course_quiz_submission_list\",\"quiz_submission_view\":\"course_quiz_submission_view\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(12, 'course_question', '{\"course_question\":\"course_question_list\",\"course_question_create\":\"course_question_create\",\"course_question_store\":\"course_question_store\",\"course_question_update\":\"course_question_update\",\"course_question_delete\":\"course_question_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(13, 'enroll', '{\"list\":\"enroll_list\",\"enroll_invoice\":\"enroll_invoice\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(14, 'certificate', '{\"list\":\"certificate_list\",\"view\":\"certificate_view\",\"download\":\"certificate_download\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(15, 'certificate_template', '{\"read\":\"certificate_template_read\",\"create\":\"certificate_template_create\",\"store\":\"certificate_template_store\",\"update\":\"certificate_template_update\",\"delete\":\"certificate_template_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(16, 'instructor', '{\"read\":\"instructor_list\",\"instructor_request_list\":\"instructor_request_list\",\"instructor_view\":\"instructor_view\",\"instructor_approve\":\"instructor_approve\",\"instructor_suspend\":\"instructor_suspend\",\"instructor_suspend_list\":\"instructor_suspend_list\",\"instructor_re_activate\":\"instructor_re_activate\",\"create\":\"instructor_create\",\"store\":\"instructor_store\",\"update\":\"instructor_update\",\"instructor_login\":\"instructor_login\",\"instructor_add_institute\":\"instructor_add_institute\",\"instructor_store_institute\":\"instructor_store_institute\",\"instructor_update_institute\":\"instructor_update_institute\",\"instructor_delete_institute\":\"instructor_delete_institute\",\"instructor_add_experience\":\"instructor_add_experience\",\"instructor_store_experience\":\"instructor_store_experience\",\"instructor_update_experience\":\"instructor_update_experience\",\"instructor_delete_experience\":\"instructor_delete_experience\",\"instructor_add_skill\":\"instructor_add_skill\",\"instructor_store_skill\":\"instructor_store_skill\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(17, 'student', '{\"read\":\"student_list\",\"student_suspend\":\"student_suspend\",\"student_re_activate\":\"student_re_activate\",\"create\":\"student_create\",\"store\":\"student_store\",\"update\":\"student_update\",\"student_login\":\"student_login\",\"student_add_institute\":\"student_add_institute\",\"student_store_institute\":\"student_store_institute\",\"student_update_institute\":\"student_update_institute\",\"student_delete_institute\":\"student_delete_institute\",\"student_add_experience\":\"student_add_experience\",\"student_store_experience\":\"student_store_experience\",\"student_update_experience\":\"student_update_experience\",\"student_delete_experience\":\"student_delete_experience\",\"student_add_skill\":\"student_add_skill\",\"student_store_skill\":\"student_store_skill\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(18, 'review', '{\"read\":\"review_list\",\"review_view\":\"review_view\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(19, 'payouts', '{\"instructor_payout_list\":\"instructor_payout_list\",\"instructor_payout_request_list\":\"instructor_payout_request_list\",\"instructor_unpaid_payout_list\":\"instructor_unpaid_payout_list\",\"instructor_rejected_payout_list\":\"instructor_rejected_payout_list\",\"instructor_payout_details\":\"instructor_payout_details\",\"instructor_payout_request_approve\":\"instructor_payout_request_approve\",\"instructor_payout_request_reject\":\"instructor_payout_request_reject\",\"instructor_make_payout\":\"instructor_make_payout\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(20, 'account', '{\"read\":\"account_list\",\"create\":\"account_create\",\"store\":\"account_store\",\"update\":\"account_update\",\"delete\":\"account_delete\",\"income_list\":\"income_list\",\"expense_list\":\"expense_list\",\"transaction_list\":\"transaction_list\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(21, 'featured_course', '{\"read\":\"featured_course_list\",\"create\":\"featured_course_create\",\"store\":\"featured_course_store\",\"update\":\"featured_course_update\",\"delete\":\"featured_course_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(22, 'discount_course', '{\"read\":\"discount_course_list\",\"create\":\"discount_course_create\",\"store\":\"discount_course_store\",\"update\":\"discount_course_update\",\"delete\":\"discount_course_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(23, 'reports', '{\"report_student_engagement\":\"report_student_engagement\",\"report_student_engagement_export\":\"report_student_engagement_export\",\"report_instructor_engagement\":\"report_instructor_engagement\",\"report_instructor_engagement_export\":\"report_instructor_engagement_export\",\"report_purchase_history\":\"report_purchase_history\",\"report_purchase_history_export\":\"report_purchase_history_export\",\"report_course_completion\":\"report_course_completion\",\"report_course_completion_export\":\"report_course_completion_export\",\"report_student_performance\":\"report_student_performance\",\"report_student_performance_export\":\"report_student_performance_export\",\"report_admin_transaction\":\"report_admin_transaction\",\"report_admin_transaction_export\":\"report_admin_transaction_export\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(24, 'testimonial', '{\"read\":\"testimonial_list\",\"create\":\"testimonial_create\",\"store\":\"testimonial_store\",\"update\":\"testimonial_update\",\"delete\":\"testimonial_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(25, 'home_section_settings', '{\"read\":\"home_section_settings_read\",\"create\":\"home_section_settings_create\",\"store\":\"home_section_settings_store\",\"update\":\"home_section_settings_update\",\"delete\":\"home_section_settings_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(26, 'footer_menu', '{\"read\":\"footer_menu_read\",\"create\":\"footer_menu_create\",\"store\":\"footer_menu_store\",\"update\":\"footer_menu_update\",\"delete\":\"footer_menu_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(27, 'payment_method', '{\"read\":\"payment_method_read\",\"update\":\"payment_method_update\",\"delete\":\"payment_method_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(28, 'general settings', '{\"read\":\"general_settings_read\",\"update\":\"general_settings_update\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(29, 'storage settings', '{\"read\":\"storage_settings_read\",\"update\":\"storage_settings_update\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(30, 'email settings', '{\"read\":\"email_settings_read\",\"update\":\"email_settings_update\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(31, 'seo settings', '{\"read\":\"seo_settings_read\",\"update\":\"seo_settings_update\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(32, 'blog_category', '{\"read\":\"blog_category_read\",\"create\":\"blog_category_create\",\"store\":\"blog_category_store\",\"update\":\"blog_category_update\",\"delete\":\"blog_category_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(33, 'blog', '{\"read\":\"blog_read\",\"create\":\"blog_create\",\"store\":\"blog_store\",\"update\":\"blog_update\",\"delete\":\"blog_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(34, 'slider', '{\"read\":\"slider_read\",\"create\":\"slider_create\",\"store\":\"slider_store\",\"update\":\"slider_update\",\"delete\":\"slider_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(35, 'page', '{\"read\":\"page_read\",\"create\":\"page_create\",\"store\":\"page_store\",\"update\":\"page_update\",\"delete\":\"page_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(36, 'brand', '{\"read\":\"brand_read\",\"create\":\"brand_create\",\"store\":\"brand_store\",\"update\":\"brand_update\",\"delete\":\"brand_delete\"}', '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `personal_access_tokens`
--

CREATE TABLE `personal_access_tokens` (
  `id` bigint UNSIGNED NOT NULL,
  `tokenable_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tokenable_id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `abilities` text COLLATE utf8mb4_unicode_ci,
  `last_used_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` bigint UNSIGNED NOT NULL,
  `title` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `quiz_id` bigint UNSIGNED DEFAULT NULL,
  `course_id` bigint UNSIGNED DEFAULT NULL,
  `type` tinyint NOT NULL DEFAULT '0' COMMENT '0 = single and true/false, 1 = multiple',
  `total_options` int NOT NULL DEFAULT '0',
  `options` longtext COLLATE utf8mb4_unicode_ci,
  `answer` longtext COLLATE utf8mb4_unicode_ci,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_by` bigint UNSIGNED DEFAULT NULL,
  `order` int NOT NULL DEFAULT '1',
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `title`, `quiz_id`, `course_id`, `type`, `total_options`, `options`, `answer`, `status_id`, `created_by`, `updated_by`, `deleted_by`, `order`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Question 1', 2, 1, 0, 4, '\"[\\\"Option 1\\\",\\\"Option 2\\\",\\\"Option 3\\\",\\\"Option 4\\\"]\"', '\"[\\\"Option 1\\\"]\"', 1, 5, 1, NULL, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Question 2', 2, 1, 1, 4, '\"[\\\"Option 1\\\",\\\"Option 2\\\",\\\"Option 3\\\",\\\"Option 4\\\"]\"', '\"[\\\"Option 1\\\",\\\"Option 2\\\"]\"', 1, 5, 1, NULL, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `question_submits`
--

CREATE TABLE `question_submits` (
  `id` bigint UNSIGNED NOT NULL,
  `question_id` bigint UNSIGNED DEFAULT NULL,
  `quiz_result_id` bigint UNSIGNED DEFAULT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `answer` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_correct` tinyint NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `quiz_results`
--

CREATE TABLE `quiz_results` (
  `id` bigint UNSIGNED NOT NULL,
  `quiz_id` bigint UNSIGNED DEFAULT NULL,
  `enroll_id` bigint UNSIGNED DEFAULT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `marks` double(8,2) NOT NULL DEFAULT '0.00',
  `total_marks` double(8,2) NOT NULL DEFAULT '0.00',
  `point` double(8,2) NOT NULL DEFAULT '0.00',
  `is_submitted` bigint UNSIGNED NOT NULL DEFAULT '10',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` bigint UNSIGNED NOT NULL,
  `rating` double(2,1) NOT NULL DEFAULT '0.0',
  `comment` text COLLATE utf8mb4_unicode_ci,
  `course_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '1',
  `permissions` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `status`, `permissions`, `created_at`, `updated_at`) VALUES
(1, 'Super Admin', '1', '[\"user_read\",\"user_create\",\"user_update\",\"user_delete\",\"role_read\",\"role_create\",\"role_update\",\"role_delete\",\"language_read\",\"language_create\",\"language_update\",\"language_update_terms\",\"language_delete\",\"general_settings_read\",\"general_settings_update\",\"storage_settings_read\",\"storage_settings_update\",\"email_settings_read\",\"email_settings_update\"]', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(2, 'Admin', '1', '[\"user_read\",\"user_create\",\"user_update\",\"user_delete\",\"role_read\",\"role_create\",\"role_update\",\"role_delete\",\"language_read\",\"language_create\",\"language_update_terms\",\"general_settings_read\",\"general_settings_update\",\"storage_settings_read\",\"storage_settings_read\",\"recaptcha_settings_update\",\"email_settings_read\"]', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(3, 'Manager', '1', '[\"user_read\",\"user_create\",\"role_read\",\"language_read\",\"language_create\",\"general_settings_read\",\"storage_settings_read\",\"email_settings_read\"]', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(4, 'Student', '1', '[\"user_read\",\"role_read\",\"language_read\"]', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(5, 'Instructor', '1', NULL, '2023-05-01 23:30:31', '2023-05-01 23:30:31');

-- --------------------------------------------------------

--
-- Table structure for table `searches`
--

CREATE TABLE `searches` (
  `id` bigint UNSIGNED NOT NULL,
  `url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `searches`
--

INSERT INTO `searches` (`id`, `url`, `created_at`, `updated_at`) VALUES
(1, 'dashboard', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'users', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'languages', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'general-settings', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(5, 'email-setting', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(6, 'dashboard1', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(7, 'pricing-table', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(8, 'pricing-table-2', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(9, 'pricing-table-3', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(10, 'pricing-table-4', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(11, 'form-elements', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(12, 'input-group', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(13, 'form-validations', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(14, 'signin', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(15, 'signup', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(16, 'reset-password', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(17, 'recover-password', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(18, 'tables', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(19, 'datatable', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(20, 'promotional', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(21, 'promotional-2', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(22, 'greetings', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(23, 'greetings-2', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(24, 'reset-password-email', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(25, 'email-verify', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(26, 'email-approved', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(27, 'deactive-account', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(28, 'terms-conditions', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(29, 'content-grid', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(30, 'colors', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(31, 'profile', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(32, 'error-page403', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(33, 'error-page404', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(34, 'error-page500', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(35, 'error-page502', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(36, 'error-coming-soon', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(37, 'error-maintenance', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(38, 'basic-timeline', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(39, 'split-timeline', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(40, 'centered-timeline', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(41, 'apex-chart', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(42, 'chartjs', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(43, 'dashboard-cards', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(44, 'product-lists', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(45, 'product-grids', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(46, 'categories', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(47, 'add-category', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(48, 'orders', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(49, 'order-detsils', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(50, 'invoice', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(51, 'line-awesome', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(52, 'line-icon', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(53, 'font-awesome', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(54, 'alert', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(55, 'progress', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(56, 'notification', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(57, 'chat', '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `sections`
--

CREATE TABLE `sections` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `course_id` bigint UNSIGNED DEFAULT NULL,
  `order` int NOT NULL DEFAULT '1',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '3',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sections`
--

INSERT INTO `sections` (`id`, `title`, `course_id`, `order`, `status_id`, `created_by`, `updated_by`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Section 1', 1, 1, 1, 5, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Section 2', 1, 2, 1, 5, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'Section 3', 1, 3, 1, 5, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'Section 4', 1, 4, 1, 5, 1, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE `settings` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `value` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `settings`
--

INSERT INTO `settings` (`id`, `name`, `value`, `created_at`, `updated_at`) VALUES
(1, 'application_name', 'Onest Academy', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'application_details', 'Lorem ipsum dolor sit amet consectetur. Morbi cras sodales elementum sed. Suspendisse adipiscing arcu magna leo sodales pellentesque. Ac iaculis mattis ornare rhoncus nibh mollis arcu.', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'footer_text', '© 2023 Onest Academy . All rights reserved.', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'file_system', 'local', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(5, 'aws_access_key_id', 'AKIA3OGN2RWSOIIG3A4J', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(6, 'aws_secret_key', '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', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(7, 'aws_region', 'ap-southeast-1', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(8, 'aws_bucket', 'onest-starter-kit', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(9, 'aws_endpoint', 'https://s3.ap-southeast-1.amazonaws.com', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(10, 'recaptcha_sitekey', '6Lfn6nQhAAAAAKYauxvLddLtcqSn1yqn-HRn_CbN', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(11, 'recaptcha_secret', '6Lfn6nQhAAAAABOzRtEjhZYB49Dd4orv41thfh02', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(12, 'recaptcha_status', '0', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(13, 'mail_drive', 'smtp', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(14, 'mail_host', 'smtp.gmail.com', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(15, 'mail_address', 'sales@onesttech.com', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(16, 'from_name', 'O-Academy', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(17, 'mail_username', 'sales@onesttech.com', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(18, 'firebase_key', '', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(19, 'country', 'Bangladesh', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(20, 'mail_password', 'eyJpdiI6InZVOTZESW5KZWQ4ZjNVcTVuL1RPb2c9PSIsInZhbHVlIjoiVnFlc1BsVnZjSjcySzJZdEg3aHVuOUJBcDh5MWVGVmU2V0dCcXUrU2lCST0iLCJtYWMiOiI2Y2ZlODNiMjFhZDM2NDljNmE5OWU4ZjY2NGM2NmYwNmE1ODY1YzJjNmIwN2MwZGNhNzVkNWIzYzQxYTdjM2FlIiwidGFnIjoiIn0=', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(21, 'mail_port', '587', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(22, 'encryption', 'tls', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(23, 'default_language', 'en', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(24, 'currency', 'USD', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(25, 'currency_symbol', '$', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(26, 'light_logo', 'uploads/backend/uploads/settings/light_logo2023-04-13-m3zlgbczk1iu-original.png', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(27, 'dark_logo', 'uploads/backend/uploads/settings/dark_logo2023-04-13-6fftzbk9pefm-original.png', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(28, 'favicon', 'uploads/backend/uploads/settings/favicon2023-04-13-ukjghc1c6zf3-original.png', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(29, 'date_format', 'd-m-Y', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(30, 'author', 'Onest Tech', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(31, 'meta_keyword', 'lms, academy, eclass, elearning, education, online course,  learning management system, live class, live meeting, lms, online education, online teaching, udemy, quiz, school, skillshare', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(32, 'meta_description', 'Onest academy - Learning Management System web application. web-based responsive application that includes an online learning management system, as well as admin, instructor panel and student panel. This is a completely ready-to-use learning management sy', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(33, 'email_address', 'info@onesttech.com', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(34, 'phone_number', '+880 1711 111 111', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(35, 'office_address', 'Dhaka, Bangladesh', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(36, 'office_hours', 'Monday - Friday : 10:00am to 6:00pm', '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(37, 'application_map', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3176328.0190763366!2d-108.19558402634385!3d38.972343352127425!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x874014749b1856b7%3A0xc75483314990a7ff!2sColorado%2C%20USA!5e0!3m2!1sen!2sbd!4v168258633', '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `sliders`
--

CREATE TABLE `sliders` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sub_title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `serial` bigint UNSIGNED NOT NULL,
  `button_text` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `button_url` text COLLATE utf8mb4_unicode_ci,
  `image_id` bigint UNSIGNED DEFAULT NULL,
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_by` bigint UNSIGNED DEFAULT NULL,
  `updated_by` bigint UNSIGNED DEFAULT NULL,
  `deleted_by` bigint UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sliders`
--

INSERT INTO `sliders` (`id`, `title`, `sub_title`, `description`, `serial`, `button_text`, `button_url`, `image_id`, `status_id`, `created_by`, `updated_by`, `deleted_by`, `created_at`, `updated_at`) VALUES
(1, 'Make yourself one', 'Comfort & Professional', '<p>comprehensive educational experiences that develop and enhance skill sets that can be applied to diverse job profiles.</p>', 1, 'Find your desired Course', '#', 5, 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Make yourself two', 'Comfort & Professional', '<p>comprehensive educational experiences that develop and enhance skill sets that can be applied to diverse job profiles.</p>', 2, 'Find your desired Course', '#', 6, 1, 1, NULL, NULL, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `statuses`
--

CREATE TABLE `statuses` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'hare name=status situation',
  `class` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'hare class=what type of class name property like success,danger,info,purple',
  `color_code` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `statuses`
--

INSERT INTO `statuses` (`id`, `name`, `class`, `color_code`, `created_at`, `updated_at`) VALUES
(1, 'Active', 'success', '449d44', NULL, NULL),
(2, 'Inactive', 'danger', 'c9302c', NULL, NULL),
(3, 'Pending', 'warning', 'ec971f', NULL, NULL),
(4, 'Approve', 'success', '449d44', NULL, NULL),
(5, 'Suspended', 'danger', 'c9302c', NULL, NULL),
(6, 'Reject', 'danger', 'c9302c', NULL, NULL),
(7, 'Cancel', 'danger', 'c9302c', NULL, NULL),
(8, 'Paid', 'success', '449d44', NULL, NULL),
(9, 'Unpaid', 'danger', 'c9302c', NULL, NULL),
(10, 'No', 'danger', 'c9302c', NULL, NULL),
(11, 'Yes', 'primary', '337ab7', NULL, NULL),
(12, 'Live', 'success', '449d44', NULL, NULL),
(13, 'Recorded', 'primary', '337ab7', NULL, NULL),
(14, 'Text', 'warning', 'ec971f', NULL, NULL),
(15, 'Youtube', 'primary', '337ab7', NULL, NULL),
(16, 'Vimeo', 'primary', '337ab7', NULL, NULL),
(17, 'Html5', 'primary', '337ab7', NULL, NULL),
(18, 'Beginner', 'primary', '337ab7', NULL, NULL),
(19, 'Intermediate', 'success', '449d44', NULL, NULL),
(20, 'Advanced', 'danger', 'c9302c', NULL, NULL),
(21, 'Draft', 'warning', 'ec971f', NULL, NULL),
(22, 'Public', 'success', '449d44', NULL, NULL),
(23, 'Private', 'danger', 'c9302c', NULL, NULL),
(24, 'Fail', 'danger', 'c9302c', NULL, NULL),
(25, 'Passed', 'success', '449d44', NULL, NULL),
(26, 'Credit', 'success', '449d44', NULL, NULL),
(27, 'Debit', 'danger', 'c9302c', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` bigint UNSIGNED NOT NULL,
  `about_me` longtext COLLATE utf8mb4_unicode_ci,
  `designation` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` tinyint NOT NULL DEFAULT '1' COMMENT '1 = male',
  `date_of_birth` date DEFAULT NULL,
  `badges` json DEFAULT NULL,
  `education` json DEFAULT NULL,
  `experience` json DEFAULT NULL,
  `skills` json DEFAULT NULL,
  `points` int NOT NULL DEFAULT '0',
  `country_id` bigint UNSIGNED DEFAULT NULL,
  `user_id` bigint UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `about_me`, `designation`, `address`, `gender`, `date_of_birth`, `badges`, `education`, `experience`, `skills`, `points`, `country_id`, `user_id`, `created_at`, `updated_at`) VALUES
(1, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, 0, NULL, 4, '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(2, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, 0, NULL, 6, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `testimonials`
--

CREATE TABLE `testimonials` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `designation` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_id` bigint UNSIGNED DEFAULT NULL,
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `rating` int NOT NULL DEFAULT '0',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `testimonials`
--

INSERT INTO `testimonials` (`id`, `name`, `designation`, `image_id`, `content`, `rating`, `status_id`, `created_at`, `updated_at`) VALUES
(1, 'Carter Stroman', 'Food Science Technician', NULL, 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation', 2, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(2, 'Mr. Reece Armstrong II', 'Fabric Mender', NULL, 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation', 2, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(3, 'Alexandrine Moen V', 'Commercial Diver', NULL, 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation', 2, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32'),
(4, 'Prof. Leanne Towne', 'Electronic Equipment Assembler', NULL, 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation', 1, 1, '2023-05-01 23:30:32', '2023-05-01 23:30:32');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` bigint UNSIGNED NOT NULL,
  `account_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `status_id` bigint UNSIGNED NOT NULL,
  `amount` double(16,2) NOT NULL DEFAULT '0.00',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `uploads`
--

CREATE TABLE `uploads` (
  `id` bigint UNSIGNED NOT NULL,
  `original` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` enum('image','video','file') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'image',
  `paths` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `uploads`
--

INSERT INTO `uploads` (`id`, `original`, `name`, `type`, `paths`, `created_at`, `updated_at`) VALUES
(1, 'uploads/course/thumbnail/thumbnail2023-04-13-to5axxqasson-original.png', '2023-04-13-to5axxqasson-original.png', 'image', '{\"100x100\": \"uploads/course/thumbnail/thumbnail2023-04-13-mrapgambbsqb-1.webp\", \"300x300\": \"uploads/course/thumbnail/thumbnail2023-04-13-ssemawxwatwi-2.webp\", \"600x600\": \"uploads/course/thumbnail/thumbnail2023-04-13-zoteupq6k2af-3.webp\"}', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(2, 'uploads/course/thumbnail/thumbnail2023-04-13-67gbgvli0ooj-original.png', '2023-04-13-67gbgvli0ooj-original.png', 'image', '{\"100x100\": \"uploads/course/thumbnail/thumbnail2023-04-13-gnyqm9ok9rcf-1.webp\", \"300x300\": \"uploads/course/thumbnail/thumbnail2023-04-13-rppkxjknxjfk-2.webp\", \"600x600\": \"uploads/course/thumbnail/thumbnail2023-04-13-ad2l5d0jbgk6-3.webp\"}', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(3, 'uploads/course/thumbnail/thumbnail2023-04-13-5r22kjvcbfkk-original.png', '2023-04-13-5r22kjvcbfkk-original.png', 'image', '{\"100x100\": \"uploads/course/thumbnail/thumbnail2023-04-13-qxfmj1njozsw-1.webp\", \"300x300\": \"uploads/course/thumbnail/thumbnail2023-04-13-vwljkji1m1l2-2.webp\", \"600x600\": \"uploads/course/thumbnail/thumbnail2023-04-13-yikrimugcafa-3.webp\"}', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(4, 'uploads/course/thumbnail/thumbnail2023-04-13-0r9v3tr0wq9v-original.png', '2023-04-13-0r9v3tr0wq9v-original.png', 'image', '{\"100x100\": \"uploads/course/thumbnail/thumbnail2023-04-13-urqgtr9aojjh-1.webp\", \"300x300\": \"uploads/course/thumbnail/thumbnail2023-04-13-mo6blahalsqk-2.webp\", \"600x600\": \"uploads/course/thumbnail/thumbnail2023-04-13-hkoqrf1vfwdi-3.webp\"}', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(5, 'uploads/Slider/image/images2023-04-13-3jkxoroofhj3-original.jpeg', '2023-04-13-3jkxoroofhj3-original.jpeg', 'image', '{\"400x1260\": \"uploads/Slider/image/images2023-04-13-jtaqj3rbr0ww-1.webp\"}', '2023-05-01 23:30:31', '2023-05-01 23:30:31'),
(6, 'uploads/Slider/image/images2023-04-13-bwzfnilgbx8b-original.jpeg', '2023-04-13-bwzfnilgbx8b-original.jpeg', 'image', '{\"400x1260\": \"uploads/Slider/image/images2023-04-13-lak8ajwixm1l-1.webp\"}', '2023-05-01 23:30:31', '2023-05-01 23:30:31');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` tinyint NOT NULL DEFAULT '1',
  `email_verified_at` timestamp NULL DEFAULT NULL COMMENT 'if null then verifield, not null then not verified',
  `token` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Token for email/phone verification, if null then verifield, not null then not verified',
  `phone` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `permissions` text COLLATE utf8mb4_unicode_ci,
  `last_login` timestamp NULL DEFAULT NULL,
  `status` tinyint NOT NULL DEFAULT '1',
  `status_id` bigint UNSIGNED NOT NULL DEFAULT '3',
  `image_id` bigint UNSIGNED DEFAULT NULL,
  `role_id` bigint UNSIGNED DEFAULT NULL,
  `designation_id` bigint UNSIGNED DEFAULT NULL,
  `device_token` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `remember_token` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `date_of_birth`, `gender`, `email_verified_at`, `token`, `phone`, `password`, `permissions`, `last_login`, `status`, `status_id`, `image_id`, `role_id`, `designation_id`, `device_token`, `remember_token`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'Super Admin', 'superadmin@onest.com', '2022-09-07', 1, '2023-05-01 23:30:31', NULL, '01811000000', '$2y$10$woAW9WzVxIIUznbTvdsYOuv/3kbaHwSuBC4B6FiK4IE2QubhgD8fe', '[\"user_read\",\"user_create\",\"user_update\",\"user_delete\",\"role_read\",\"role_create\",\"role_update\",\"role_delete\",\"ai_support\",\"ai_support_find\",\"course_category_read\",\"course_category_store\",\"course_category_create\",\"course_category_update\",\"course_category_delete\",\"popular_course_category_list\",\"popular_course_category_added\",\"popular_course_category_deleted\",\"course_read\",\"course_store\",\"course_create\",\"course_update\",\"course_delete\",\"course_assignment_list\",\"course_assignment_create\",\"course_assignment_store\",\"course_assignment_update\",\"course_assignment_delete\",\"course_assignment_submission_list\",\"course_assignment_submission_view\",\"course_noticeboard_list\",\"course_noticeboard_create\",\"course_noticeboard_store\",\"course_noticeboard_update\",\"course_noticeboard_delete\",\"course_announcement_list\",\"course_curriculum\",\"course_curriculum_create\",\"course_curriculum_store\",\"course_curriculum_update\",\"course_curriculum_delete\",\"course_lesson\",\"course_lesson_create\",\"course_lesson_store\",\"course_lesson_update\",\"course_lesson_delete\",\"course_quiz_list\",\"course_quiz_create\",\"course_quiz_store\",\"course_quiz_update\",\"course_quiz_delete\",\"course_question_list\",\"course_question_create\",\"course_question_store\",\"course_question_update\",\"course_question_delete\",\"enroll_list\",\"enroll_invoice\",\"certificate_list\",\"certificate_view\",\"certificate_download\",\"instructor_list\",\"instructor_request_list\",\"instructor_view\",\"instructor_approve\",\"instructor_suspend\",\"instructor_suspend_list\",\"instructor_re_activate\",\"instructor_create\",\"instructor_store\",\"instructor_update\",\"instructor_login\",\"instructor_add_institute\",\"instructor_store_institute\",\"instructor_update_institute\",\"instructor_delete_institute\",\"instructor_add_experience\",\"instructor_store_experience\",\"instructor_update_experience\",\"instructor_delete_experience\",\"instructor_add_skill\",\"instructor_store_skill\",\"student_list\",\"student_suspend\",\"student_re_activate\",\"student_create\",\"student_store\",\"student_update\",\"student_login\",\"student_add_institute\",\"student_store_institute\",\"student_update_institute\",\"student_delete_institute\",\"student_add_experience\",\"student_store_experience\",\"student_update_experience\",\"student_delete_experience\",\"student_add_skill\",\"student_store_skill\",\"certificate_template_read\",\"certificate_template_create\",\"certificate_template_update\",\"certificate_template_delete\",\"review_list\",\"review_view\",\"instructor_payout_list\",\"instructor_payout_request_list\",\"instructor_unpaid_payout_list\",\"instructor_rejected_payout_list\",\"instructor_payout_details\",\"instructor_payout_request_approve\",\"instructor_payout_request_reject\",\"instructor_make_payout\",\"account_list\",\"account_create\",\"account_store\",\"account_update\",\"account_delete\",\"income_list\",\"expense_list\",\"transaction_list\",\"featured_course_list\",\"featured_course_create\",\"featured_course_store\",\"featured_course_update\",\"featured_course_delete\",\"discount_course_list\",\"discount_course_create\",\"discount_course_store\",\"discount_course_update\",\"discount_course_delete\",\"report_student_engagement\",\"report_student_engagement_export\",\"report_instructor_engagement\",\"report_instructor_engagement_export\",\"report_purchase_history\",\"report_purchase_history_export\",\"report_course_completion\",\"report_course_completion_export\",\"report_admin_transaction\",\"report_admin_transaction_export\",\"language_read\",\"language_create\",\"language_update\",\"language_update_terms\",\"language_delete\",\"general_settings_read\",\"general_settings_update\",\"storage_settings_read\",\"storage_settings_update\",\"email_settings_read\",\"email_settings_update\",\"testimonial_read\",\"testimonial_create\",\"testimonial_store\",\"testimonial_update\",\"testimonial_delete\",\"blog_category_read\",\"blog_category_store\",\"blog_category_create\",\"blog_category_update\",\"blog_category_delete\",\"blog_read\",\"blog_store\",\"blog_create\",\"blog_update\",\"blog_delete\",\"slider_read\",\"slider_store\",\"slider_create\",\"slider_update\",\"slider_delete\",\"page_read\",\"page_store\",\"page_create\",\"page_update\",\"page_delete\",\"brand_read\",\"brand_store\",\"brand_create\",\"brand_update\",\"brand_delete\",\"payment_method_read\",\"payment_method_update\",\"payment_method_delete\",\"home_section_settings_read\",\"home_section_settings_create\",\"home_section_settings_store\",\"home_section_settings_update\",\"home_section_settings_delete\",\"footer_menu_read\",\"footer_menu_store\",\"footer_menu_create\",\"footer_menu_update\",\"footer_menu_delete\"]', NULL, 1, 4, NULL, 1, 1, NULL, 'xhwJMbIpNP', '2023-05-01 23:30:31', '2023-05-01 23:30:31', NULL),
(2, 'admin', 'admin@onest.com', '2022-09-07', 1, '2023-05-01 23:30:31', NULL, '01811000001', '$2y$10$LZEp.YB5LhiIPLnDhaBe9ua42gCgXhf8ORxiDMiuHx9w8DSAJ1fPq', '[\"user_read\",\"user_create\",\"user_update\",\"user_delete\",\"role_read\",\"role_create\",\"role_update\",\"role_delete\",\"language_read\",\"language_create\",\"language_update_terms\",\"general_settings_read\",\"general_settings_update\",\"storage_settings_read\",\"storage_settings_read\",\"recaptcha_settings_update\",\"email_settings_read\"]', NULL, 1, 4, NULL, 2, 1, NULL, 'Fakle3udVp', '2023-05-01 23:30:31', '2023-05-01 23:30:31', NULL),
(3, 'Anna Littlical', 'manager@onest.com', '2022-09-07', 1, '2023-05-01 23:30:31', NULL, '01811000002', '$2y$10$NbfweoIqCAp0U4I.mS8q2eVgiUc5D0M5kqrsa3HuUc73k//ocMxcS', '[\"user_read\",\"user_create\",\"role_read\",\"language_read\",\"language_create\",\"general_settings_read\",\"storage_settings_read\",\"email_settings_read\"]', NULL, 1, 4, NULL, 3, 5, NULL, 'R50afjhMHh', '2023-05-01 23:30:31', '2023-05-01 23:30:31', NULL),
(4, 'student1', 'student@onest.com', '2022-09-07', 1, '2023-05-01 23:30:31', NULL, '1345789784561', '$2y$10$URXM6WSupWYSC3k6qNMTu.NHFgzkS6CjUP2/5WbmzX26J2i5/476q', '[\"user_read\",\"role_read\",\"language_read\"]', NULL, 1, 4, NULL, 4, 4, NULL, 'i5sYBvELmY', '2023-05-01 23:30:31', '2023-05-01 23:30:31', NULL),
(5, 'instructor', 'instructor@onest.com', '2022-09-07', 1, '2023-05-01 23:30:31', NULL, '13457897', '$2y$10$kV/Ybt7rx48xopKbpASWmOSdMtji800SVrhpdbLZvS4I9agw16ZeO', NULL, NULL, 1, 4, NULL, 5, 5, NULL, 'ofWiHsglpJ', '2023-05-01 23:30:32', '2023-05-01 23:30:32', NULL),
(6, 'student-2', 'student-2@onest.com', '2022-09-07', 1, '2023-05-01 23:30:32', NULL, '134578978400', '$2y$10$gY6b8hdaXxHn2N1aX1ko2u35IZro/DOtyMU/ZSC5EtjhHsMVDtRtq', '[\"user_read\",\"role_read\",\"language_read\"]', NULL, 1, 3, NULL, 4, 3, NULL, 'HgDO3OIQBo', '2023-05-01 23:30:32', '2023-05-01 23:30:32', NULL),
(7, 'instructor 1', 'instructor1@onest.com', '2022-09-07', 1, '2023-05-01 23:30:32', NULL, '1345789001', '$2y$10$NzFXCd6sxP92MB3qi7iVG.P4QDelCXWiD4QU2PT0moC5tiuv4PvNu', NULL, NULL, 1, 3, NULL, 5, 5, NULL, '8IYkQJjqzm', '2023-05-01 23:30:32', '2023-05-01 23:30:32', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accounts_status_id_foreign` (`status_id`);

--
-- Indexes for table `app_home_sections`
--
ALTER TABLE `app_home_sections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_home_sections_status_id_foreign` (`status_id`);

--
-- Indexes for table `assignments`
--
ALTER TABLE `assignments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `assignments_course_id_foreign` (`course_id`),
  ADD KEY `assignments_assignment_file_foreign` (`assignment_file`),
  ADD KEY `assignments_created_by_foreign` (`created_by`),
  ADD KEY `assignments_updated_by_foreign` (`updated_by`),
  ADD KEY `course_id` (`title`),
  ADD KEY `assignments_status_id_index` (`status_id`);

--
-- Indexes for table `assignment_submits`
--
ALTER TABLE `assignment_submits`
  ADD PRIMARY KEY (`id`),
  ADD KEY `assignment_submits_enroll_id_foreign` (`enroll_id`),
  ADD KEY `assignment_submits_status_id_foreign` (`status_id`),
  ADD KEY `assignment_submits_assignment_file_foreign` (`assignment_file`),
  ADD KEY `enroll_id` (`assignment_id`),
  ADD KEY `assignment_submits_is_submitted_index` (`is_submitted`),
  ADD KEY `assignment_submits_user_id_index` (`user_id`);

--
-- Indexes for table `blogs`
--
ALTER TABLE `blogs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `blogs_slug_unique` (`slug`),
  ADD KEY `blogs_image_id_foreign` (`image_id`),
  ADD KEY `blogs_status_id_foreign` (`status_id`),
  ADD KEY `blogs_blog_categories_id_foreign` (`blog_categories_id`),
  ADD KEY `blogs_created_by_foreign` (`created_by`),
  ADD KEY `blogs_updated_by_foreign` (`updated_by`),
  ADD KEY `blogs_deleted_by_foreign` (`deleted_by`),
  ADD KEY `blogs_meta_image_id_foreign` (`meta_image_id`),
  ADD KEY `blogs_title_status_id_blog_categories_id_created_by_index` (`title`,`status_id`,`blog_categories_id`,`created_by`);

--
-- Indexes for table `blog_categories`
--
ALTER TABLE `blog_categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `blog_categories_slug_unique` (`slug`),
  ADD KEY `blog_categories_status_id_foreign` (`status_id`),
  ADD KEY `blog_categories_created_by_foreign` (`created_by`),
  ADD KEY `status_id` (`title`);

--
-- Indexes for table `bookmarks`
--
ALTER TABLE `bookmarks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bookmarks_user_id_foreign` (`user_id`),
  ADD KEY `bookmarks_course_id_user_id_index` (`course_id`,`user_id`);

--
-- Indexes for table `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `brands_serial_unique` (`serial`),
  ADD KEY `brands_image_id_foreign` (`image_id`),
  ADD KEY `brands_created_by_foreign` (`created_by`),
  ADD KEY `brands_updated_by_foreign` (`updated_by`),
  ADD KEY `brands_deleted_by_foreign` (`deleted_by`),
  ADD KEY `brands_status_id_created_by_serial_index` (`status_id`,`created_by`,`serial`);

--
-- Indexes for table `carts`
--
ALTER TABLE `carts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `carts_user_id_foreign` (`user_id`),
  ADD KEY `carts_course_id_user_id_index` (`course_id`,`user_id`);

--
-- Indexes for table `certificate_generates`
--
ALTER TABLE `certificate_generates`
  ADD PRIMARY KEY (`id`),
  ADD KEY `certificate_generates_user_id_foreign` (`user_id`),
  ADD KEY `certificate_generates_upload_id_foreign` (`upload_id`),
  ADD KEY `certificate_generates_enroll_id_foreign` (`enroll_id`);

--
-- Indexes for table `certificate_templates`
--
ALTER TABLE `certificate_templates`
  ADD PRIMARY KEY (`id`),
  ADD KEY `certificate_templates_image_id_foreign` (`image_id`),
  ADD KEY `certificate_templates_default_id_foreign` (`default_id`),
  ADD KEY `certificate_templates_status_id_foreign` (`status_id`),
  ADD KEY `certificate_templates_font_id_foreign` (`font_id`);

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `countries`
--
ALTER TABLE `countries`
  ADD PRIMARY KEY (`id`),
  ADD KEY `countries_currency_name_index` (`currency`,`name`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `courses_slug_unique` (`slug`),
  ADD KEY `courses_course_category_id_foreign` (`course_category_id`),
  ADD KEY `courses_meta_image_foreign` (`meta_image`),
  ADD KEY `courses_thumbnail_foreign` (`thumbnail`),
  ADD KEY `courses_course_overview_type_foreign` (`course_overview_type`),
  ADD KEY `courses_course_type_foreign` (`course_type`),
  ADD KEY `courses_instructor_id_foreign` (`instructor_id`),
  ADD KEY `courses_level_id_foreign` (`level_id`),
  ADD KEY `courses_visibility_id_foreign` (`visibility_id`),
  ADD KEY `courses_created_by_foreign` (`created_by`),
  ADD KEY `courses_updated_by_foreign` (`updated_by`),
  ADD KEY `courses_deleted_by_foreign` (`deleted_by`),
  ADD KEY `is_free` (`title`),
  ADD KEY `instructor_id` (`status_id`);

--
-- Indexes for table `course_categories`
--
ALTER TABLE `course_categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_categories_icon_foreign` (`icon`),
  ADD KEY `course_categories_thumbnail_foreign` (`thumbnail`),
  ADD KEY `course_categories_parent_id_foreign` (`parent_id`),
  ADD KEY `course_categories_user_id_foreign` (`user_id`),
  ADD KEY `course_categories_status_id_foreign` (`status_id`),
  ADD KEY `status_id` (`title`);

--
-- Indexes for table `currencies`
--
ALTER TABLE `currencies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `date_formats`
--
ALTER TABLE `date_formats`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `designations`
--
ALTER TABLE `designations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `enrolls`
--
ALTER TABLE `enrolls`
  ADD PRIMARY KEY (`id`),
  ADD KEY `enrolls_course_id_foreign` (`course_id`),
  ADD KEY `enrolls_user_id_foreign` (`user_id`),
  ADD KEY `enrolls_order_item_id_course_id_user_id_index` (`order_item_id`,`course_id`,`user_id`),
  ADD KEY `enrolls_instructor_id_index` (`instructor_id`);

--
-- Indexes for table `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `expenses_transaction_id_foreign` (`transaction_id`),
  ADD KEY `expenses_status_id_foreign` (`status_id`);

--
-- Indexes for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`);

--
-- Indexes for table `featured_courses`
--
ALTER TABLE `featured_courses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `featured_courses_status_id_foreign` (`status_id`),
  ADD KEY `featured_courses_course_id_status_id_index` (`course_id`,`status_id`);

--
-- Indexes for table `flag_icons`
--
ALTER TABLE `flag_icons`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `footer_menus`
--
ALTER TABLE `footer_menus`
  ADD PRIMARY KEY (`id`),
  ADD KEY `footer_menus_status_id_foreign` (`status_id`);

--
-- Indexes for table `incomes`
--
ALTER TABLE `incomes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `incomes_transaction_id_foreign` (`transaction_id`),
  ADD KEY `incomes_status_id_foreign` (`status_id`);

--
-- Indexes for table `instructors`
--
ALTER TABLE `instructors`
  ADD PRIMARY KEY (`id`),
  ADD KEY `instructors_country_id_foreign` (`country_id`),
  ADD KEY `instructors_user_id_country_id_index` (`user_id`,`country_id`);

--
-- Indexes for table `instructor_payment_methods`
--
ALTER TABLE `instructor_payment_methods`
  ADD PRIMARY KEY (`id`),
  ADD KEY `instructor_payment_methods_status_id_foreign` (`status_id`),
  ADD KEY `instructor_payment_methods_user_id_index` (`user_id`),
  ADD KEY `instructor_payment_methods_payment_method_id_is_default_index` (`payment_method_id`,`is_default`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobs_queue_index` (`queue`);

--
-- Indexes for table `languages`
--
ALTER TABLE `languages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `lessons`
--
ALTER TABLE `lessons`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lessons_video_file_foreign` (`video_file`),
  ADD KEY `lessons_attachment_foreign` (`attachment`),
  ADD KEY `lessons_image_file_foreign` (`image_file`),
  ADD KEY `lessons_created_by_foreign` (`created_by`),
  ADD KEY `lessons_updated_by_foreign` (`updated_by`),
  ADD KEY `lessons_status_id_foreign` (`status_id`),
  ADD KEY `is_free` (`title`),
  ADD KEY `lessons_section_id_index` (`section_id`),
  ADD KEY `order` (`course_id`),
  ADD KEY `lessons_is_quiz_index` (`is_quiz`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notes`
--
ALTER TABLE `notes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `notes_lesson_id_foreign` (`lesson_id`),
  ADD KEY `notes_user_id_foreign` (`user_id`),
  ADD KEY `notes_enroll_id_lesson_id_user_id_index` (`enroll_id`,`lesson_id`,`user_id`);

--
-- Indexes for table `notice_boards`
--
ALTER TABLE `notice_boards`
  ADD PRIMARY KEY (`id`),
  ADD KEY `notice_boards_course_id_foreign` (`course_id`),
  ADD KEY `notice_boards_status_id_foreign` (`status_id`),
  ADD KEY `notice_boards_created_by_foreign` (`created_by`),
  ADD KEY `notice_boards_updated_by_foreign` (`updated_by`),
  ADD KEY `course_id` (`title`),
  ADD KEY `status_id` (`is_send_mail`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `orders_user_id_payment_method_invoice_number_status_index` (`user_id`,`payment_method`,`invoice_number`,`status`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_items_course_id_foreign` (`course_id`),
  ADD KEY `order_items_order_id_course_id_index` (`order_id`,`course_id`);

--
-- Indexes for table `pages`
--
ALTER TABLE `pages`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `pages_slug_unique` (`slug`),
  ADD KEY `pages_status_id_foreign` (`status_id`),
  ADD KEY `pages_created_by_foreign` (`created_by`),
  ADD KEY `pages_updated_by_foreign` (`updated_by`),
  ADD KEY `pages_deleted_by_foreign` (`deleted_by`),
  ADD KEY `pages_title_slug_status_id_created_by_index` (`title`,`slug`,`status_id`,`created_by`);

--
-- Indexes for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD KEY `password_resets_email_index` (`email`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `payments_invoice_number_unique` (`invoice_number`),
  ADD KEY `payments_user_id_foreign` (`user_id`),
  ADD KEY `payments_payout_id_foreign` (`payout_id`);

--
-- Indexes for table `payment_methods`
--
ALTER TABLE `payment_methods`
  ADD PRIMARY KEY (`id`),
  ADD KEY `payment_methods_image_id_foreign` (`image_id`),
  ADD KEY `payment_methods_status_id_foreign` (`status_id`),
  ADD KEY `payment_methods_title_name_index` (`title`,`name`);

--
-- Indexes for table `payouts`
--
ALTER TABLE `payouts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `payouts_user_id_foreign` (`user_id`),
  ADD KEY `payouts_instructor_payment_method_id_foreign` (`instructor_payment_method_id`),
  ADD KEY `payouts_status_id_foreign` (`status_id`),
  ADD KEY `payouts_payment_status_id_foreign` (`payment_status_id`);

--
-- Indexes for table `payout_logs`
--
ALTER TABLE `payout_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `payout_logs_payout_id_foreign` (`payout_id`),
  ADD KEY `payout_logs_status_id_foreign` (`status_id`),
  ADD KEY `payout_logs_user_id_foreign` (`user_id`);

--
-- Indexes for table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `personal_access_tokens_token_unique` (`token`),
  ADD KEY `personal_access_tokens_tokenable_type_tokenable_id_index` (`tokenable_type`,`tokenable_id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `questions_status_id_foreign` (`status_id`),
  ADD KEY `questions_created_by_foreign` (`created_by`),
  ADD KEY `questions_updated_by_foreign` (`updated_by`),
  ADD KEY `questions_deleted_by_foreign` (`deleted_by`),
  ADD KEY `questions_quiz_id_index` (`quiz_id`),
  ADD KEY `status_id` (`course_id`),
  ADD KEY `order` (`type`);

--
-- Indexes for table `question_submits`
--
ALTER TABLE `question_submits`
  ADD PRIMARY KEY (`id`),
  ADD KEY `question_submits_question_id_foreign` (`question_id`),
  ADD KEY `question_submits_quiz_result_id_foreign` (`quiz_result_id`),
  ADD KEY `question_submits_user_id_foreign` (`user_id`);

--
-- Indexes for table `quiz_results`
--
ALTER TABLE `quiz_results`
  ADD PRIMARY KEY (`id`),
  ADD KEY `quiz_results_enroll_id_foreign` (`enroll_id`),
  ADD KEY `quiz_results_status_id_foreign` (`status_id`),
  ADD KEY `quiz_results_quiz_id_index` (`quiz_id`),
  ADD KEY `quiz_results_user_id_index` (`user_id`),
  ADD KEY `status_id` (`is_submitted`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reviews_user_id_foreign` (`user_id`),
  ADD KEY `reviews_status_id_foreign` (`status_id`),
  ADD KEY `reviews_course_id_user_id_rating_index` (`course_id`,`user_id`,`rating`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `searches`
--
ALTER TABLE `searches`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sections`
--
ALTER TABLE `sections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sections_created_by_foreign` (`created_by`),
  ADD KEY `sections_updated_by_foreign` (`updated_by`),
  ADD KEY `sections_title_index` (`title`),
  ADD KEY `order` (`course_id`),
  ADD KEY `sections_status_id_index` (`status_id`);

--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `settings_name_unique` (`name`);

--
-- Indexes for table `sliders`
--
ALTER TABLE `sliders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sliders_serial_unique` (`serial`),
  ADD KEY `sliders_image_id_foreign` (`image_id`),
  ADD KEY `sliders_status_id_foreign` (`status_id`),
  ADD KEY `sliders_created_by_foreign` (`created_by`),
  ADD KEY `sliders_updated_by_foreign` (`updated_by`),
  ADD KEY `sliders_deleted_by_foreign` (`deleted_by`),
  ADD KEY `sliders_title_sub_title_status_id_created_by_serial_index` (`title`,`sub_title`,`status_id`,`created_by`,`serial`);

--
-- Indexes for table `statuses`
--
ALTER TABLE `statuses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `statuses_name_class_index` (`name`,`class`),
  ADD KEY `statuses_name_index` (`name`),
  ADD KEY `statuses_class_index` (`class`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD KEY `students_country_id_foreign` (`country_id`),
  ADD KEY `students_user_id_country_id_index` (`user_id`,`country_id`);

--
-- Indexes for table `testimonials`
--
ALTER TABLE `testimonials`
  ADD PRIMARY KEY (`id`),
  ADD KEY `testimonials_image_id_foreign` (`image_id`),
  ADD KEY `testimonials_status_id_foreign` (`status_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `transactions_account_id_foreign` (`account_id`),
  ADD KEY `transactions_user_id_foreign` (`user_id`),
  ADD KEY `transactions_status_id_foreign` (`status_id`);

--
-- Indexes for table `uploads`
--
ALTER TABLE `uploads`
  ADD PRIMARY KEY (`id`),
  ADD KEY `type` (`original`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`),
  ADD KEY `users_status_id_foreign` (`status_id`),
  ADD KEY `users_image_id_foreign` (`image_id`),
  ADD KEY `users_role_id_foreign` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `app_home_sections`
--
ALTER TABLE `app_home_sections`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `assignments`
--
ALTER TABLE `assignments`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `assignment_submits`
--
ALTER TABLE `assignment_submits`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blogs`
--
ALTER TABLE `blogs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `blog_categories`
--
ALTER TABLE `blog_categories`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `bookmarks`
--
ALTER TABLE `bookmarks`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `brands`
--
ALTER TABLE `brands`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `carts`
--
ALTER TABLE `carts`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `certificate_generates`
--
ALTER TABLE `certificate_generates`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `certificate_templates`
--
ALTER TABLE `certificate_templates`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `countries`
--
ALTER TABLE `countries`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=253;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `course_categories`
--
ALTER TABLE `course_categories`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `currencies`
--
ALTER TABLE `currencies`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT for table `date_formats`
--
ALTER TABLE `date_formats`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `designations`
--
ALTER TABLE `designations`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `enrolls`
--
ALTER TABLE `enrolls`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `featured_courses`
--
ALTER TABLE `featured_courses`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `flag_icons`
--
ALTER TABLE `flag_icons`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=250;

--
-- AUTO_INCREMENT for table `footer_menus`
--
ALTER TABLE `footer_menus`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `incomes`
--
ALTER TABLE `incomes`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `instructors`
--
ALTER TABLE `instructors`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `instructor_payment_methods`
--
ALTER TABLE `instructor_payment_methods`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `languages`
--
ALTER TABLE `languages`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `lessons`
--
ALTER TABLE `lessons`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `notes`
--
ALTER TABLE `notes`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notice_boards`
--
ALTER TABLE `notice_boards`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pages`
--
ALTER TABLE `pages`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payment_methods`
--
ALTER TABLE `payment_methods`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `payouts`
--
ALTER TABLE `payouts`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payout_logs`
--
ALTER TABLE `payout_logs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `question_submits`
--
ALTER TABLE `question_submits`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `quiz_results`
--
ALTER TABLE `quiz_results`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `searches`
--
ALTER TABLE `searches`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `sections`
--
ALTER TABLE `sections`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `settings`
--
ALTER TABLE `settings`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `sliders`
--
ALTER TABLE `sliders`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `statuses`
--
ALTER TABLE `statuses`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `testimonials`
--
ALTER TABLE `testimonials`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `uploads`
--
ALTER TABLE `uploads`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts`
--
ALTER TABLE `accounts`
  ADD CONSTRAINT `accounts_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `app_home_sections`
--
ALTER TABLE `app_home_sections`
  ADD CONSTRAINT `app_home_sections_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `assignments`
--
ALTER TABLE `assignments`
  ADD CONSTRAINT `assignments_assignment_file_foreign` FOREIGN KEY (`assignment_file`) REFERENCES `uploads` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `assignments_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `assignments_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `assignments_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `assignments_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `assignment_submits`
--
ALTER TABLE `assignment_submits`
  ADD CONSTRAINT `assignment_submits_assignment_file_foreign` FOREIGN KEY (`assignment_file`) REFERENCES `uploads` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `assignment_submits_assignment_id_foreign` FOREIGN KEY (`assignment_id`) REFERENCES `assignments` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `assignment_submits_enroll_id_foreign` FOREIGN KEY (`enroll_id`) REFERENCES `enrolls` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `assignment_submits_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `assignment_submits_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `blogs`
--
ALTER TABLE `blogs`
  ADD CONSTRAINT `blogs_blog_categories_id_foreign` FOREIGN KEY (`blog_categories_id`) REFERENCES `blog_categories` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `blogs_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `blogs_deleted_by_foreign` FOREIGN KEY (`deleted_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `blogs_image_id_foreign` FOREIGN KEY (`image_id`) REFERENCES `uploads` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `blogs_meta_image_id_foreign` FOREIGN KEY (`meta_image_id`) REFERENCES `uploads` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `blogs_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `blogs_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `blog_categories`
--
ALTER TABLE `blog_categories`
  ADD CONSTRAINT `blog_categories_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `blog_categories_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `bookmarks`
--
ALTER TABLE `bookmarks`
  ADD CONSTRAINT `bookmarks_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookmarks_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `brands`
--
ALTER TABLE `brands`
  ADD CONSTRAINT `brands_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `brands_deleted_by_foreign` FOREIGN KEY (`deleted_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `brands_image_id_foreign` FOREIGN KEY (`image_id`) REFERENCES `uploads` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `brands_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `brands_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `carts`
--
ALTER TABLE `carts`
  ADD CONSTRAINT `carts_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `carts_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `certificate_generates`
--
ALTER TABLE `certificate_generates`
  ADD CONSTRAINT `certificate_generates_enroll_id_foreign` FOREIGN KEY (`enroll_id`) REFERENCES `enrolls` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `certificate_generates_upload_id_foreign` FOREIGN KEY (`upload_id`) REFERENCES `uploads` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `certificate_generates_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `certificate_templates`
--
ALTER TABLE `certificate_templates`
  ADD CONSTRAINT `certificate_templates_default_id_foreign` FOREIGN KEY (`default_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `certificate_templates_font_id_foreign` FOREIGN KEY (`font_id`) REFERENCES `uploads` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `certificate_templates_image_id_foreign` FOREIGN KEY (`image_id`) REFERENCES `uploads` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `certificate_templates_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `courses_course_category_id_foreign` FOREIGN KEY (`course_category_id`) REFERENCES `course_categories` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_course_overview_type_foreign` FOREIGN KEY (`course_overview_type`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_course_type_foreign` FOREIGN KEY (`course_type`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_deleted_by_foreign` FOREIGN KEY (`deleted_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_instructor_id_foreign` FOREIGN KEY (`instructor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_level_id_foreign` FOREIGN KEY (`level_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_meta_image_foreign` FOREIGN KEY (`meta_image`) REFERENCES `uploads` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `courses_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_thumbnail_foreign` FOREIGN KEY (`thumbnail`) REFERENCES `uploads` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `courses_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_visibility_id_foreign` FOREIGN KEY (`visibility_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `course_categories`
--
ALTER TABLE `course_categories`
  ADD CONSTRAINT `course_categories_icon_foreign` FOREIGN KEY (`icon`) REFERENCES `uploads` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `course_categories_parent_id_foreign` FOREIGN KEY (`parent_id`) REFERENCES `course_categories` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `course_categories_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `course_categories_thumbnail_foreign` FOREIGN KEY (`thumbnail`) REFERENCES `uploads` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `course_categories_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `enrolls`
--
ALTER TABLE `enrolls`
  ADD CONSTRAINT `enrolls_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `enrolls_instructor_id_foreign` FOREIGN KEY (`instructor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `enrolls_order_item_id_foreign` FOREIGN KEY (`order_item_id`) REFERENCES `order_items` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `enrolls_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `expenses`
--
ALTER TABLE `expenses`
  ADD CONSTRAINT `expenses_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `expenses_transaction_id_foreign` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `featured_courses`
--
ALTER TABLE `featured_courses`
  ADD CONSTRAINT `featured_courses_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `featured_courses_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `footer_menus`
--
ALTER TABLE `footer_menus`
  ADD CONSTRAINT `footer_menus_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `incomes`
--
ALTER TABLE `incomes`
  ADD CONSTRAINT `incomes_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `incomes_transaction_id_foreign` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `instructors`
--
ALTER TABLE `instructors`
  ADD CONSTRAINT `instructors_country_id_foreign` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `instructors_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `instructor_payment_methods`
--
ALTER TABLE `instructor_payment_methods`
  ADD CONSTRAINT `instructor_payment_methods_payment_method_id_foreign` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_methods` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `instructor_payment_methods_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `instructor_payment_methods_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lessons`
--
ALTER TABLE `lessons`
  ADD CONSTRAINT `lessons_attachment_foreign` FOREIGN KEY (`attachment`) REFERENCES `uploads` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lessons_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lessons_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lessons_image_file_foreign` FOREIGN KEY (`image_file`) REFERENCES `uploads` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lessons_section_id_foreign` FOREIGN KEY (`section_id`) REFERENCES `sections` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lessons_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lessons_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lessons_video_file_foreign` FOREIGN KEY (`video_file`) REFERENCES `uploads` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `notes`
--
ALTER TABLE `notes`
  ADD CONSTRAINT `notes_enroll_id_foreign` FOREIGN KEY (`enroll_id`) REFERENCES `enrolls` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notes_lesson_id_foreign` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notes_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `notice_boards`
--
ALTER TABLE `notice_boards`
  ADD CONSTRAINT `notice_boards_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notice_boards_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notice_boards_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notice_boards_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_order_id_foreign` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `pages`
--
ALTER TABLE `pages`
  ADD CONSTRAINT `pages_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `pages_deleted_by_foreign` FOREIGN KEY (`deleted_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `pages_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `pages_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_payout_id_foreign` FOREIGN KEY (`payout_id`) REFERENCES `payouts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payments_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `payment_methods`
--
ALTER TABLE `payment_methods`
  ADD CONSTRAINT `payment_methods_image_id_foreign` FOREIGN KEY (`image_id`) REFERENCES `uploads` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payment_methods_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `payouts`
--
ALTER TABLE `payouts`
  ADD CONSTRAINT `payouts_instructor_payment_method_id_foreign` FOREIGN KEY (`instructor_payment_method_id`) REFERENCES `instructor_payment_methods` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payouts_payment_status_id_foreign` FOREIGN KEY (`payment_status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payouts_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payouts_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `payout_logs`
--
ALTER TABLE `payout_logs`
  ADD CONSTRAINT `payout_logs_payout_id_foreign` FOREIGN KEY (`payout_id`) REFERENCES `payouts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payout_logs_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payout_logs_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `questions_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `questions_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `questions_deleted_by_foreign` FOREIGN KEY (`deleted_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `questions_quiz_id_foreign` FOREIGN KEY (`quiz_id`) REFERENCES `lessons` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `questions_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `questions_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `question_submits`
--
ALTER TABLE `question_submits`
  ADD CONSTRAINT `question_submits_question_id_foreign` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `question_submits_quiz_result_id_foreign` FOREIGN KEY (`quiz_result_id`) REFERENCES `quiz_results` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `question_submits_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `quiz_results`
--
ALTER TABLE `quiz_results`
  ADD CONSTRAINT `quiz_results_enroll_id_foreign` FOREIGN KEY (`enroll_id`) REFERENCES `enrolls` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `quiz_results_is_submitted_foreign` FOREIGN KEY (`is_submitted`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `quiz_results_quiz_id_foreign` FOREIGN KEY (`quiz_id`) REFERENCES `lessons` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `quiz_results_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `quiz_results_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `sections`
--
ALTER TABLE `sections`
  ADD CONSTRAINT `sections_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `sections_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `sections_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `sections_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `sliders`
--
ALTER TABLE `sliders`
  ADD CONSTRAINT `sliders_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `sliders_deleted_by_foreign` FOREIGN KEY (`deleted_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `sliders_image_id_foreign` FOREIGN KEY (`image_id`) REFERENCES `uploads` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `sliders_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `sliders_updated_by_foreign` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_country_id_foreign` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `students_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `testimonials`
--
ALTER TABLE `testimonials`
  ADD CONSTRAINT `testimonials_image_id_foreign` FOREIGN KEY (`image_id`) REFERENCES `uploads` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `testimonials_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_account_id_foreign` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transactions_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transactions_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_image_id_foreign` FOREIGN KEY (`image_id`) REFERENCES `uploads` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `users_role_id_foreign` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `users_status_id_foreign` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
