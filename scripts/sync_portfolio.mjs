// ポートフォリオサイトのリポジトリから掲載内容を読み出し、data/portfolio.json に書き出す。
//
// 使い方（ポートフォリオのリポジトリで npm install 済みであること）:
//     node scripts/sync_portfolio.mjs [../portfolio]
//
// 読むのは掲載中の作品（repos.ts の listedProjects）とプロフィール・技術一覧だけ。
// 限定公開の repos.unlisted.ts は読まない。
// 氏名はプロフィール README に出さないため書き出さない。
import { execFileSync } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const portfolio = resolve(process.argv[2] ?? resolve(here, "../../portfolio"));
const out = resolve(here, "../data/portfolio.json");

const code = `
import { profile } from "./src/content/profile.ts";
import { listedProjects, sortedProjects } from "./src/content/repos.ts";
import { techs } from "./src/content/tech.ts";
const projects = sortedProjects(listedProjects()).map((p) => ({
  slug: p.slug,
  title: p.title,
  tagline: p.tagline,
  description: p.description,
  createdAt: p.createdAt,
  status: p.status,
  primaryLang: p.primaryLang,
  tech: p.tech,
  highlights: p.highlights,
}));
console.log(JSON.stringify({
  tagline: profile.tagline,
  bio: profile.bio,
  socialLinks: profile.socialLinks,
  techs: techs.map(({ id, label, category, learning }) => ({ id, label, category, learning: !!learning })),
  projects,
}));
`;

const json = execFileSync(resolve(portfolio, "node_modules/.bin/tsx"), ["--eval", code], {
  cwd: portfolio,
  encoding: "utf8",
});
const data = JSON.parse(json);
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, JSON.stringify(data, null, 2) + "\n");
console.log(`${data.projects.length} projects → ${out}`);
