const CANONICAL_HOST = "www.jgjpaystock.com";
const APEX_HOST = CANONICAL_HOST.startsWith("www.") ? CANONICAL_HOST.slice(4) : CANONICAL_HOST;
const DEFAULT_LANG = "fr";
const SUPPORTED_LANGS = ["fr", "en", "de"];
const DEFAULT_BILLING_API = "https://api.jgjpaystock.com";

function pickLanguage(acceptLanguage, defaultLang) {
  if (!acceptLanguage) return defaultLang;
  const lower = acceptLanguage.toLowerCase();
  if (/\bde\b/.test(lower) || /\bde-/.test(lower)) return "de";
  if (/\ben\b/.test(lower) || /\ben-/.test(lower)) return "en";
  if (/\bfr\b/.test(lower) || /\bfr-/.test(lower)) return "fr";
  return defaultLang;
}

export function onRequest({ request, next, env }) {
  const url = new URL(request.url);
  const canonicalHost = (env && env.CANONICAL_HOST) || CANONICAL_HOST;
  const apexHost = canonicalHost.startsWith("www.") ? canonicalHost.slice(4) : canonicalHost;
  const defaultLang = (env && env.DEFAULT_LANGUAGE) || DEFAULT_LANG;

  if (url.hostname === apexHost && url.hostname !== canonicalHost) {
    url.hostname = canonicalHost;
    return Response.redirect(url.toString(), 301);
  }

  if (url.hostname !== canonicalHost) {
    return next();
  }

  // Serve /config.js dynamically from env vars - never hardcode URLs in HTML
  if (url.pathname === "/config.js") {
    const billingApi = (env && env.BILLING_API_URL) || DEFAULT_BILLING_API;
    const siteOrigin = (env && env.SITE_ORIGIN) || `${url.origin}`;
    const js = `window.__ENV__={BILLING_API:${JSON.stringify(billingApi)},SITE_ORIGIN:${JSON.stringify(siteOrigin)}};`;
    return new Response(js, {
      headers: {
        "Content-Type": "application/javascript; charset=utf-8",
        "Cache-Control": "no-store",
      },
    });
  }

  if (url.pathname === "/" || url.pathname === "/index.html") {
    const lang = pickLanguage(request.headers.get("accept-language"), defaultLang);
    return Response.redirect(`${url.origin}/${lang}/`, 302);
  }

  if (SUPPORTED_LANGS.includes(url.pathname.slice(1))) {
    return Response.redirect(`${url.origin}${url.pathname}/`, 301);
  }

  if (
    url.pathname === "/about.html" ||
    url.pathname === "/contact.html" ||
    url.pathname === "/faq.html" ||
    url.pathname === "/features.html" ||
    url.pathname === "/pricing.html"
  ) {
    return Response.redirect(`${url.origin}/${defaultLang}${url.pathname.replace(/\.html$/, "")}`, 301);
  }

  return next();
}
