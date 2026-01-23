import { Hero, HowItWorks, Models, Features, Privacy, Testimonials, CTA } from '../components/home';

export default function Home() {
  return (
    <main style={{ paddingTop: '80px' }}>
      <Hero />
      <HowItWorks />
      <Models />
      <Features />
      <Privacy />
      <Testimonials />
      <CTA />
    </main>
  );
}
