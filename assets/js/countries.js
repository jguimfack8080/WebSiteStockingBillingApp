/*
 * countries.js - Liste complete des pays du monde (ISO 3166-1 alpha-2)
 * + combobox recherchable accessible pour le selecteur de pays a l'inscription.
 *
 * - Noms localises (fr / en / de). La valeur soumise est le code ISO alpha-2
 *   (normalise, independant de la langue) -> le backend en deduit la devise.
 * - Tri alphabetique selon la langue de la page.
 * - Recherche insensible aux accents et a la casse.
 *
 * Source unique cote site. Le backend maintient sa propre table code -> devise.
 */
(function (global) {
  'use strict';

  // code: ISO 3166-1 alpha-2 ; en/fr/de: nom localise ; ccy: ISO 4217 (info).
  var COUNTRIES = [
    { code: 'AF', en: 'Afghanistan', fr: 'Afghanistan', de: 'Afghanistan', ccy: 'AFN' },
    { code: 'ZA', en: 'South Africa', fr: 'Afrique du Sud', de: 'Sudafrika', ccy: 'ZAR' },
    { code: 'AL', en: 'Albania', fr: 'Albanie', de: 'Albanien', ccy: 'ALL' },
    { code: 'DZ', en: 'Algeria', fr: 'Algerie', de: 'Algerien', ccy: 'DZD' },
    { code: 'DE', en: 'Germany', fr: 'Allemagne', de: 'Deutschland', ccy: 'EUR' },
    { code: 'AD', en: 'Andorra', fr: 'Andorre', de: 'Andorra', ccy: 'EUR' },
    { code: 'AO', en: 'Angola', fr: 'Angola', de: 'Angola', ccy: 'AOA' },
    { code: 'AG', en: 'Antigua and Barbuda', fr: 'Antigua-et-Barbuda', de: 'Antigua und Barbuda', ccy: 'XCD' },
    { code: 'SA', en: 'Saudi Arabia', fr: 'Arabie saoudite', de: 'Saudi-Arabien', ccy: 'SAR' },
    { code: 'AR', en: 'Argentina', fr: 'Argentine', de: 'Argentinien', ccy: 'ARS' },
    { code: 'AM', en: 'Armenia', fr: 'Armenie', de: 'Armenien', ccy: 'AMD' },
    { code: 'AU', en: 'Australia', fr: 'Australie', de: 'Australien', ccy: 'AUD' },
    { code: 'AT', en: 'Austria', fr: 'Autriche', de: 'Osterreich', ccy: 'EUR' },
    { code: 'AZ', en: 'Azerbaijan', fr: 'Azerbaidjan', de: 'Aserbaidschan', ccy: 'AZN' },
    { code: 'BS', en: 'Bahamas', fr: 'Bahamas', de: 'Bahamas', ccy: 'BSD' },
    { code: 'BH', en: 'Bahrain', fr: 'Bahrein', de: 'Bahrain', ccy: 'BHD' },
    { code: 'BD', en: 'Bangladesh', fr: 'Bangladesh', de: 'Bangladesch', ccy: 'BDT' },
    { code: 'BB', en: 'Barbados', fr: 'Barbade', de: 'Barbados', ccy: 'BBD' },
    { code: 'BE', en: 'Belgium', fr: 'Belgique', de: 'Belgien', ccy: 'EUR' },
    { code: 'BZ', en: 'Belize', fr: 'Belize', de: 'Belize', ccy: 'BZD' },
    { code: 'BJ', en: 'Benin', fr: 'Benin', de: 'Benin', ccy: 'XOF' },
    { code: 'BT', en: 'Bhutan', fr: 'Bhoutan', de: 'Bhutan', ccy: 'BTN' },
    { code: 'BY', en: 'Belarus', fr: 'Bielorussie', de: 'Belarus', ccy: 'BYN' },
    { code: 'BO', en: 'Bolivia', fr: 'Bolivie', de: 'Bolivien', ccy: 'BOB' },
    { code: 'BA', en: 'Bosnia and Herzegovina', fr: 'Bosnie-Herzegovine', de: 'Bosnien und Herzegowina', ccy: 'BAM' },
    { code: 'BW', en: 'Botswana', fr: 'Botswana', de: 'Botswana', ccy: 'BWP' },
    { code: 'BR', en: 'Brazil', fr: 'Bresil', de: 'Brasilien', ccy: 'BRL' },
    { code: 'BN', en: 'Brunei', fr: 'Brunei', de: 'Brunei', ccy: 'BND' },
    { code: 'BG', en: 'Bulgaria', fr: 'Bulgarie', de: 'Bulgarien', ccy: 'BGN' },
    { code: 'BF', en: 'Burkina Faso', fr: 'Burkina Faso', de: 'Burkina Faso', ccy: 'XOF' },
    { code: 'BI', en: 'Burundi', fr: 'Burundi', de: 'Burundi', ccy: 'BIF' },
    { code: 'KH', en: 'Cambodia', fr: 'Cambodge', de: 'Kambodscha', ccy: 'KHR' },
    { code: 'CM', en: 'Cameroon', fr: 'Cameroun', de: 'Kamerun', ccy: 'XAF' },
    { code: 'CA', en: 'Canada', fr: 'Canada', de: 'Kanada', ccy: 'CAD' },
    { code: 'CV', en: 'Cape Verde', fr: 'Cap-Vert', de: 'Kap Verde', ccy: 'CVE' },
    { code: 'CL', en: 'Chile', fr: 'Chili', de: 'Chile', ccy: 'CLP' },
    { code: 'CN', en: 'China', fr: 'Chine', de: 'China', ccy: 'CNY' },
    { code: 'CY', en: 'Cyprus', fr: 'Chypre', de: 'Zypern', ccy: 'EUR' },
    { code: 'CO', en: 'Colombia', fr: 'Colombie', de: 'Kolumbien', ccy: 'COP' },
    { code: 'KM', en: 'Comoros', fr: 'Comores', de: 'Komoren', ccy: 'KMF' },
    { code: 'CG', en: 'Congo (Republic)', fr: 'Congo (Republique)', de: 'Kongo (Republik)', ccy: 'XAF' },
    { code: 'CD', en: 'Congo (DR)', fr: 'Congo (RD)', de: 'Kongo (DR)', ccy: 'CDF' },
    { code: 'KR', en: 'South Korea', fr: 'Coree du Sud', de: 'Sudkorea', ccy: 'KRW' },
    { code: 'KP', en: 'North Korea', fr: 'Coree du Nord', de: 'Nordkorea', ccy: 'KPW' },
    { code: 'CR', en: 'Costa Rica', fr: 'Costa Rica', de: 'Costa Rica', ccy: 'CRC' },
    { code: 'CI', en: "Cote d'Ivoire", fr: "Cote d'Ivoire", de: 'Elfenbeinkuste', ccy: 'XOF' },
    { code: 'HR', en: 'Croatia', fr: 'Croatie', de: 'Kroatien', ccy: 'EUR' },
    { code: 'CU', en: 'Cuba', fr: 'Cuba', de: 'Kuba', ccy: 'CUP' },
    { code: 'DK', en: 'Denmark', fr: 'Danemark', de: 'Danemark', ccy: 'DKK' },
    { code: 'DJ', en: 'Djibouti', fr: 'Djibouti', de: 'Dschibuti', ccy: 'DJF' },
    { code: 'DM', en: 'Dominica', fr: 'Dominique', de: 'Dominica', ccy: 'XCD' },
    { code: 'EG', en: 'Egypt', fr: 'Egypte', de: 'Agypten', ccy: 'EGP' },
    { code: 'AE', en: 'United Arab Emirates', fr: 'Emirats arabes unis', de: 'Vereinigte Arabische Emirate', ccy: 'AED' },
    { code: 'EC', en: 'Ecuador', fr: 'Equateur', de: 'Ecuador', ccy: 'USD' },
    { code: 'ER', en: 'Eritrea', fr: 'Erythree', de: 'Eritrea', ccy: 'ERN' },
    { code: 'ES', en: 'Spain', fr: 'Espagne', de: 'Spanien', ccy: 'EUR' },
    { code: 'EE', en: 'Estonia', fr: 'Estonie', de: 'Estland', ccy: 'EUR' },
    { code: 'SZ', en: 'Eswatini', fr: 'Eswatini', de: 'Eswatini', ccy: 'SZL' },
    { code: 'US', en: 'United States', fr: 'Etats-Unis', de: 'Vereinigte Staaten', ccy: 'USD' },
    { code: 'ET', en: 'Ethiopia', fr: 'Ethiopie', de: 'Athiopien', ccy: 'ETB' },
    { code: 'FJ', en: 'Fiji', fr: 'Fidji', de: 'Fidschi', ccy: 'FJD' },
    { code: 'FI', en: 'Finland', fr: 'Finlande', de: 'Finnland', ccy: 'EUR' },
    { code: 'FR', en: 'France', fr: 'France', de: 'Frankreich', ccy: 'EUR' },
    { code: 'GA', en: 'Gabon', fr: 'Gabon', de: 'Gabun', ccy: 'XAF' },
    { code: 'GM', en: 'Gambia', fr: 'Gambie', de: 'Gambia', ccy: 'GMD' },
    { code: 'GE', en: 'Georgia', fr: 'Georgie', de: 'Georgien', ccy: 'GEL' },
    { code: 'GH', en: 'Ghana', fr: 'Ghana', de: 'Ghana', ccy: 'GHS' },
    { code: 'GR', en: 'Greece', fr: 'Grece', de: 'Griechenland', ccy: 'EUR' },
    { code: 'GD', en: 'Grenada', fr: 'Grenade', de: 'Grenada', ccy: 'XCD' },
    { code: 'GT', en: 'Guatemala', fr: 'Guatemala', de: 'Guatemala', ccy: 'GTQ' },
    { code: 'GN', en: 'Guinea', fr: 'Guinee', de: 'Guinea', ccy: 'GNF' },
    { code: 'GW', en: 'Guinea-Bissau', fr: 'Guinee-Bissau', de: 'Guinea-Bissau', ccy: 'XOF' },
    { code: 'GQ', en: 'Equatorial Guinea', fr: 'Guinee equatoriale', de: 'Aquatorialguinea', ccy: 'XAF' },
    { code: 'GY', en: 'Guyana', fr: 'Guyana', de: 'Guyana', ccy: 'GYD' },
    { code: 'HT', en: 'Haiti', fr: 'Haiti', de: 'Haiti', ccy: 'HTG' },
    { code: 'HN', en: 'Honduras', fr: 'Honduras', de: 'Honduras', ccy: 'HNL' },
    { code: 'HU', en: 'Hungary', fr: 'Hongrie', de: 'Ungarn', ccy: 'HUF' },
    { code: 'IN', en: 'India', fr: 'Inde', de: 'Indien', ccy: 'INR' },
    { code: 'ID', en: 'Indonesia', fr: 'Indonesie', de: 'Indonesien', ccy: 'IDR' },
    { code: 'IQ', en: 'Iraq', fr: 'Irak', de: 'Irak', ccy: 'IQD' },
    { code: 'IR', en: 'Iran', fr: 'Iran', de: 'Iran', ccy: 'IRR' },
    { code: 'IE', en: 'Ireland', fr: 'Irlande', de: 'Irland', ccy: 'EUR' },
    { code: 'IS', en: 'Iceland', fr: 'Islande', de: 'Island', ccy: 'ISK' },
    { code: 'IL', en: 'Israel', fr: 'Israel', de: 'Israel', ccy: 'ILS' },
    { code: 'IT', en: 'Italy', fr: 'Italie', de: 'Italien', ccy: 'EUR' },
    { code: 'JM', en: 'Jamaica', fr: 'Jamaique', de: 'Jamaika', ccy: 'JMD' },
    { code: 'JP', en: 'Japan', fr: 'Japon', de: 'Japan', ccy: 'JPY' },
    { code: 'JO', en: 'Jordan', fr: 'Jordanie', de: 'Jordanien', ccy: 'JOD' },
    { code: 'KZ', en: 'Kazakhstan', fr: 'Kazakhstan', de: 'Kasachstan', ccy: 'KZT' },
    { code: 'KE', en: 'Kenya', fr: 'Kenya', de: 'Kenia', ccy: 'KES' },
    { code: 'KG', en: 'Kyrgyzstan', fr: 'Kirghizistan', de: 'Kirgisistan', ccy: 'KGS' },
    { code: 'KI', en: 'Kiribati', fr: 'Kiribati', de: 'Kiribati', ccy: 'AUD' },
    { code: 'KW', en: 'Kuwait', fr: 'Koweit', de: 'Kuwait', ccy: 'KWD' },
    { code: 'LA', en: 'Laos', fr: 'Laos', de: 'Laos', ccy: 'LAK' },
    { code: 'LS', en: 'Lesotho', fr: 'Lesotho', de: 'Lesotho', ccy: 'LSL' },
    { code: 'LV', en: 'Latvia', fr: 'Lettonie', de: 'Lettland', ccy: 'EUR' },
    { code: 'LB', en: 'Lebanon', fr: 'Liban', de: 'Libanon', ccy: 'LBP' },
    { code: 'LR', en: 'Liberia', fr: 'Liberia', de: 'Liberia', ccy: 'LRD' },
    { code: 'LY', en: 'Libya', fr: 'Libye', de: 'Libyen', ccy: 'LYD' },
    { code: 'LI', en: 'Liechtenstein', fr: 'Liechtenstein', de: 'Liechtenstein', ccy: 'CHF' },
    { code: 'LT', en: 'Lithuania', fr: 'Lituanie', de: 'Litauen', ccy: 'EUR' },
    { code: 'LU', en: 'Luxembourg', fr: 'Luxembourg', de: 'Luxemburg', ccy: 'EUR' },
    { code: 'MK', en: 'North Macedonia', fr: 'Macedoine du Nord', de: 'Nordmazedonien', ccy: 'MKD' },
    { code: 'MG', en: 'Madagascar', fr: 'Madagascar', de: 'Madagaskar', ccy: 'MGA' },
    { code: 'MY', en: 'Malaysia', fr: 'Malaisie', de: 'Malaysia', ccy: 'MYR' },
    { code: 'MW', en: 'Malawi', fr: 'Malawi', de: 'Malawi', ccy: 'MWK' },
    { code: 'MV', en: 'Maldives', fr: 'Maldives', de: 'Malediven', ccy: 'MVR' },
    { code: 'ML', en: 'Mali', fr: 'Mali', de: 'Mali', ccy: 'XOF' },
    { code: 'MT', en: 'Malta', fr: 'Malte', de: 'Malta', ccy: 'EUR' },
    { code: 'MA', en: 'Morocco', fr: 'Maroc', de: 'Marokko', ccy: 'MAD' },
    { code: 'MH', en: 'Marshall Islands', fr: 'Iles Marshall', de: 'Marshallinseln', ccy: 'USD' },
    { code: 'MU', en: 'Mauritius', fr: 'Maurice', de: 'Mauritius', ccy: 'MUR' },
    { code: 'MR', en: 'Mauritania', fr: 'Mauritanie', de: 'Mauretanien', ccy: 'MRU' },
    { code: 'MX', en: 'Mexico', fr: 'Mexique', de: 'Mexiko', ccy: 'MXN' },
    { code: 'FM', en: 'Micronesia', fr: 'Micronesie', de: 'Mikronesien', ccy: 'USD' },
    { code: 'MD', en: 'Moldova', fr: 'Moldavie', de: 'Moldau', ccy: 'MDL' },
    { code: 'MC', en: 'Monaco', fr: 'Monaco', de: 'Monaco', ccy: 'EUR' },
    { code: 'MN', en: 'Mongolia', fr: 'Mongolie', de: 'Mongolei', ccy: 'MNT' },
    { code: 'ME', en: 'Montenegro', fr: 'Montenegro', de: 'Montenegro', ccy: 'EUR' },
    { code: 'MZ', en: 'Mozambique', fr: 'Mozambique', de: 'Mosambik', ccy: 'MZN' },
    { code: 'MM', en: 'Myanmar', fr: 'Birmanie', de: 'Myanmar', ccy: 'MMK' },
    { code: 'NA', en: 'Namibia', fr: 'Namibie', de: 'Namibia', ccy: 'NAD' },
    { code: 'NR', en: 'Nauru', fr: 'Nauru', de: 'Nauru', ccy: 'AUD' },
    { code: 'NP', en: 'Nepal', fr: 'Nepal', de: 'Nepal', ccy: 'NPR' },
    { code: 'NI', en: 'Nicaragua', fr: 'Nicaragua', de: 'Nicaragua', ccy: 'NIO' },
    { code: 'NE', en: 'Niger', fr: 'Niger', de: 'Niger', ccy: 'XOF' },
    { code: 'NG', en: 'Nigeria', fr: 'Nigeria', de: 'Nigeria', ccy: 'NGN' },
    { code: 'NO', en: 'Norway', fr: 'Norvege', de: 'Norwegen', ccy: 'NOK' },
    { code: 'NZ', en: 'New Zealand', fr: 'Nouvelle-Zelande', de: 'Neuseeland', ccy: 'NZD' },
    { code: 'OM', en: 'Oman', fr: 'Oman', de: 'Oman', ccy: 'OMR' },
    { code: 'UG', en: 'Uganda', fr: 'Ouganda', de: 'Uganda', ccy: 'UGX' },
    { code: 'UZ', en: 'Uzbekistan', fr: 'Ouzbekistan', de: 'Usbekistan', ccy: 'UZS' },
    { code: 'PK', en: 'Pakistan', fr: 'Pakistan', de: 'Pakistan', ccy: 'PKR' },
    { code: 'PW', en: 'Palau', fr: 'Palaos', de: 'Palau', ccy: 'USD' },
    { code: 'PS', en: 'Palestine', fr: 'Palestine', de: 'Palastina', ccy: 'ILS' },
    { code: 'PA', en: 'Panama', fr: 'Panama', de: 'Panama', ccy: 'PAB' },
    { code: 'PG', en: 'Papua New Guinea', fr: 'Papouasie-Nouvelle-Guinee', de: 'Papua-Neuguinea', ccy: 'PGK' },
    { code: 'PY', en: 'Paraguay', fr: 'Paraguay', de: 'Paraguay', ccy: 'PYG' },
    { code: 'NL', en: 'Netherlands', fr: 'Pays-Bas', de: 'Niederlande', ccy: 'EUR' },
    { code: 'PE', en: 'Peru', fr: 'Perou', de: 'Peru', ccy: 'PEN' },
    { code: 'PH', en: 'Philippines', fr: 'Philippines', de: 'Philippinen', ccy: 'PHP' },
    { code: 'PL', en: 'Poland', fr: 'Pologne', de: 'Polen', ccy: 'PLN' },
    { code: 'PT', en: 'Portugal', fr: 'Portugal', de: 'Portugal', ccy: 'EUR' },
    { code: 'QA', en: 'Qatar', fr: 'Qatar', de: 'Katar', ccy: 'QAR' },
    { code: 'CF', en: 'Central African Republic', fr: 'Republique centrafricaine', de: 'Zentralafrikanische Republik', ccy: 'XAF' },
    { code: 'DO', en: 'Dominican Republic', fr: 'Republique dominicaine', de: 'Dominikanische Republik', ccy: 'DOP' },
    { code: 'CZ', en: 'Czechia', fr: 'Republique tcheque', de: 'Tschechien', ccy: 'CZK' },
    { code: 'RO', en: 'Romania', fr: 'Roumanie', de: 'Rumanien', ccy: 'RON' },
    { code: 'GB', en: 'United Kingdom', fr: 'Royaume-Uni', de: 'Vereinigtes Konigreich', ccy: 'GBP' },
    { code: 'RU', en: 'Russia', fr: 'Russie', de: 'Russland', ccy: 'RUB' },
    { code: 'RW', en: 'Rwanda', fr: 'Rwanda', de: 'Ruanda', ccy: 'RWF' },
    { code: 'KN', en: 'Saint Kitts and Nevis', fr: 'Saint-Christophe-et-Nieves', de: 'St. Kitts und Nevis', ccy: 'XCD' },
    { code: 'SM', en: 'San Marino', fr: 'Saint-Marin', de: 'San Marino', ccy: 'EUR' },
    { code: 'VC', en: 'Saint Vincent and the Grenadines', fr: 'Saint-Vincent-et-les-Grenadines', de: 'St. Vincent und die Grenadinen', ccy: 'XCD' },
    { code: 'LC', en: 'Saint Lucia', fr: 'Sainte-Lucie', de: 'St. Lucia', ccy: 'XCD' },
    { code: 'SB', en: 'Solomon Islands', fr: 'Iles Salomon', de: 'Salomonen', ccy: 'SBD' },
    { code: 'SV', en: 'El Salvador', fr: 'Salvador', de: 'El Salvador', ccy: 'USD' },
    { code: 'WS', en: 'Samoa', fr: 'Samoa', de: 'Samoa', ccy: 'WST' },
    { code: 'ST', en: 'Sao Tome and Principe', fr: 'Sao Tome-et-Principe', de: 'Sao Tome und Principe', ccy: 'STN' },
    { code: 'SN', en: 'Senegal', fr: 'Senegal', de: 'Senegal', ccy: 'XOF' },
    { code: 'RS', en: 'Serbia', fr: 'Serbie', de: 'Serbien', ccy: 'RSD' },
    { code: 'SC', en: 'Seychelles', fr: 'Seychelles', de: 'Seychellen', ccy: 'SCR' },
    { code: 'SL', en: 'Sierra Leone', fr: 'Sierra Leone', de: 'Sierra Leone', ccy: 'SLE' },
    { code: 'SG', en: 'Singapore', fr: 'Singapour', de: 'Singapur', ccy: 'SGD' },
    { code: 'SK', en: 'Slovakia', fr: 'Slovaquie', de: 'Slowakei', ccy: 'EUR' },
    { code: 'SI', en: 'Slovenia', fr: 'Slovenie', de: 'Slowenien', ccy: 'EUR' },
    { code: 'SO', en: 'Somalia', fr: 'Somalie', de: 'Somalia', ccy: 'SOS' },
    { code: 'SD', en: 'Sudan', fr: 'Soudan', de: 'Sudan', ccy: 'SDG' },
    { code: 'SS', en: 'South Sudan', fr: 'Soudan du Sud', de: 'Sudsudan', ccy: 'SSP' },
    { code: 'LK', en: 'Sri Lanka', fr: 'Sri Lanka', de: 'Sri Lanka', ccy: 'LKR' },
    { code: 'SE', en: 'Sweden', fr: 'Suede', de: 'Schweden', ccy: 'SEK' },
    { code: 'CH', en: 'Switzerland', fr: 'Suisse', de: 'Schweiz', ccy: 'CHF' },
    { code: 'SR', en: 'Suriname', fr: 'Suriname', de: 'Suriname', ccy: 'SRD' },
    { code: 'SY', en: 'Syria', fr: 'Syrie', de: 'Syrien', ccy: 'SYP' },
    { code: 'TJ', en: 'Tajikistan', fr: 'Tadjikistan', de: 'Tadschikistan', ccy: 'TJS' },
    { code: 'TZ', en: 'Tanzania', fr: 'Tanzanie', de: 'Tansania', ccy: 'TZS' },
    { code: 'TD', en: 'Chad', fr: 'Tchad', de: 'Tschad', ccy: 'XAF' },
    { code: 'TH', en: 'Thailand', fr: 'Thailande', de: 'Thailand', ccy: 'THB' },
    { code: 'TL', en: 'Timor-Leste', fr: 'Timor oriental', de: 'Timor-Leste', ccy: 'USD' },
    { code: 'TG', en: 'Togo', fr: 'Togo', de: 'Togo', ccy: 'XOF' },
    { code: 'TO', en: 'Tonga', fr: 'Tonga', de: 'Tonga', ccy: 'TOP' },
    { code: 'TT', en: 'Trinidad and Tobago', fr: 'Trinite-et-Tobago', de: 'Trinidad und Tobago', ccy: 'TTD' },
    { code: 'TN', en: 'Tunisia', fr: 'Tunisie', de: 'Tunesien', ccy: 'TND' },
    { code: 'TM', en: 'Turkmenistan', fr: 'Turkmenistan', de: 'Turkmenistan', ccy: 'TMT' },
    { code: 'TR', en: 'Turkey', fr: 'Turquie', de: 'Turkei', ccy: 'TRY' },
    { code: 'TV', en: 'Tuvalu', fr: 'Tuvalu', de: 'Tuvalu', ccy: 'AUD' },
    { code: 'UA', en: 'Ukraine', fr: 'Ukraine', de: 'Ukraine', ccy: 'UAH' },
    { code: 'UY', en: 'Uruguay', fr: 'Uruguay', de: 'Uruguay', ccy: 'UYU' },
    { code: 'VU', en: 'Vanuatu', fr: 'Vanuatu', de: 'Vanuatu', ccy: 'VUV' },
    { code: 'VA', en: 'Vatican City', fr: 'Vatican', de: 'Vatikanstadt', ccy: 'EUR' },
    { code: 'VE', en: 'Venezuela', fr: 'Venezuela', de: 'Venezuela', ccy: 'VES' },
    { code: 'VN', en: 'Vietnam', fr: 'Vietnam', de: 'Vietnam', ccy: 'VND' },
    { code: 'YE', en: 'Yemen', fr: 'Yemen', de: 'Jemen', ccy: 'YER' },
    { code: 'ZM', en: 'Zambia', fr: 'Zambie', de: 'Sambia', ccy: 'ZMW' },
    { code: 'ZW', en: 'Zimbabwe', fr: 'Zimbabwe', de: 'Simbabwe', ccy: 'ZWG' }
  ];

  // Normalisation : minuscule + suppression des accents (recherche tolerante).
  function normalize(s) {
    return (s || '').toString().normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
  }

  /**
   * Transforme un champ en combobox pays recherchable.
   * opts: { lang, hiddenId, searchId, listId, placeholder, noResults }
   * Le code ISO selectionne est ecrit dans l'input cache (hiddenId) -> soumis au backend.
   */
  function initCountryCombobox(opts) {
    var lang = (opts.lang || 'en').toLowerCase();
    var nameKey = (lang === 'fr' || lang === 'de') ? lang : 'en';
    var hidden = document.getElementById(opts.hiddenId);
    var search = document.getElementById(opts.searchId);
    var list = document.getElementById(opts.listId);
    if (!hidden || !search || !list) return;

    // Tri alphabetique selon la langue de la page.
    var items = COUNTRIES.slice().sort(function (a, b) {
      return a[nameKey].localeCompare(b[nameKey], lang);
    });

    var activeIndex = -1;
    var visible = [];

    function close() {
      list.hidden = true;
      search.setAttribute('aria-expanded', 'false');
      activeIndex = -1;
    }

    function render(filter) {
      var nf = normalize(filter);
      list.innerHTML = '';
      visible = items.filter(function (c) {
        return !nf || normalize(c[nameKey]).indexOf(nf) !== -1 || c.code.toLowerCase().indexOf(nf) === 0;
      });
      if (visible.length === 0) {
        var li = document.createElement('li');
        li.className = 'country-combo__empty';
        li.textContent = opts.noResults || 'No result';
        list.appendChild(li);
      } else {
        visible.forEach(function (c, i) {
          var li = document.createElement('li');
          li.className = 'country-combo__option';
          li.id = opts.listId + '-opt-' + i;
          li.setAttribute('role', 'option');
          li.dataset.code = c.code;
          li.textContent = c[nameKey];
          li.addEventListener('mousedown', function (e) {
            e.preventDefault();
            select(c);
          });
          list.appendChild(li);
        });
      }
      list.hidden = false;
      search.setAttribute('aria-expanded', 'true');
      activeIndex = -1;
    }

    function select(c) {
      hidden.value = c.code;
      search.value = c[nameKey];
      search.classList.remove('is-invalid');
      var err = document.querySelector('[data-for="' + opts.hiddenId + '"]');
      if (err) err.textContent = '';
      close();
    }

    function highlight(idx) {
      var nodes = list.querySelectorAll('.country-combo__option');
      nodes.forEach(function (n) { n.classList.remove('is-active'); });
      if (idx >= 0 && idx < nodes.length) {
        nodes[idx].classList.add('is-active');
        nodes[idx].scrollIntoView({ block: 'nearest' });
        search.setAttribute('aria-activedescendant', nodes[idx].id);
      }
    }

    search.addEventListener('input', function () {
      hidden.value = '';  // toute frappe invalide la selection precedente
      render(search.value);
    });
    search.addEventListener('focus', function () {
      if (list.hidden) render(search.value);
    });
    search.addEventListener('keydown', function (e) {
      if (list.hidden && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) { render(search.value); return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); activeIndex = Math.min(activeIndex + 1, visible.length - 1); highlight(activeIndex); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); activeIndex = Math.max(activeIndex - 1, 0); highlight(activeIndex); }
      else if (e.key === 'Enter') { if (!list.hidden && activeIndex >= 0 && visible[activeIndex]) { e.preventDefault(); select(visible[activeIndex]); } }
      else if (e.key === 'Escape') { close(); }
    });
    document.addEventListener('click', function (e) {
      if (!list.contains(e.target) && e.target !== search) close();
    });
  }

  // Styles du combobox injectes une seule fois (valables sur toutes les pages).
  (function injectStyles() {
    if (document.getElementById('country-combo-styles')) return;
    var css =
      '.country-combo{position:relative}' +
      '.country-combo__list{position:absolute;z-index:50;left:0;right:0;top:calc(100% + 4px);' +
      'margin:0;padding:.25rem;list-style:none;max-height:260px;overflow-y:auto;background:#fff;' +
      'border:1.5px solid var(--neutral-200);border-radius:10px;box-shadow:0 12px 32px rgba(15,23,42,.14)}' +
      '.country-combo__option{padding:.55rem .75rem;border-radius:7px;font-size:.95rem;color:var(--neutral-700);cursor:pointer}' +
      '.country-combo__option:hover,.country-combo__option.is-active{background:#eef2ff;color:#4361ee}' +
      '.country-combo__empty{padding:.65rem .75rem;font-size:.9rem;color:var(--neutral-500)}';
    var style = document.createElement('style');
    style.id = 'country-combo-styles';
    style.textContent = css;
    document.head.appendChild(style);
  })();

  global.JGJ_COUNTRIES = COUNTRIES;
  global.initCountryCombobox = initCountryCombobox;
})(window);
