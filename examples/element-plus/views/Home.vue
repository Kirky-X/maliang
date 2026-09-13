<!--
  由 draw-element 从 examples/ui-markdown/ui/home.md 生成
  组件映射(查 references/framework/element/):
    input(搜索框)        → <el-input>
    grid(金刚区)         → <el-row> + <el-col>
    navigation(顶部导航)  → 无原生移动导航对应,组合实现(<header> + 图标按钮)
    navigation(底部 dock) → 无原生 tab 栏对应,组合实现(固定 <nav> + 按钮)
    list + card(内容流)   → 组合实现(v-for 卡片;非数据表格,不映射 el-table)
    反馈                  → ElMessage(见 framework/element/message/)
  token 取值来自 examples/ui-markdown/token.md,以 CSS 变量注入 :root,
  组件内禁止硬编码色值/字号/间距(scoped 仅作作用域隔离)。
-->

<template>
  <div class="home-page">
    <header class="nav-bar">
      <button class="icon-btn" aria-label="菜单" @click="onMenu">
        <svg class="glyph glyph-ink" viewBox="0 0 24 24" aria-hidden="true">
          <line x1="4" y1="7" x2="20" y2="7" />
          <line x1="4" y1="12" x2="20" y2="12" />
          <line x1="4" y1="17" x2="14" y2="17" />
        </svg>
      </button>
      <span class="nav-title">首页</span>
      <button class="icon-btn" aria-label="消息" @click="onTab(tabs[2])">
        <svg class="glyph glyph-ink" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4 7a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H10l-4 4v-4H7a3 3 0 0 1-3-3z" />
        </svg>
        <span class="dot" aria-hidden="true"></span>
      </button>
    </header>

    <main class="page-body">
      <div class="search-pill">
        <el-input
          v-model="keyword"
          placeholder="请输入搜索的关键词"
          aria-label="搜索框"
          clearable
          @keyup.enter="onSearch"
        >
          <template #suffix>
            <svg class="glyph glyph-muted" viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="11" cy="11" r="7" />
              <line x1="16.5" y1="16.5" x2="21" y2="21" />
            </svg>
          </template>
        </el-input>
      </div>

      <el-row :gutter="16" class="entries" aria-label="金刚区入口">
        <el-col v-for="e in entries" :key="e.id" :span="8">
          <button class="entry" @click="onEntry(e)">
            <svg class="glyph glyph-brand" viewBox="0 0 24 24" aria-hidden="true" v-html="e.icon" />
            <span class="entry-label">{{ e.label }}</span>
          </button>
        </el-col>
      </el-row>

      <section class="feed" aria-label="内容流">
        <article
          v-for="c in feed"
          :key="c.id"
          class="card"
          role="button"
          tabindex="0"
          @click="onCard(c)"
          @keyup.enter="onCard(c)"
        >
          <div class="cover" :class="c.tone" aria-hidden="true"></div>
          <div class="card-body">
            <h2 class="card-title">{{ c.title }}</h2>
            <div class="card-meta">
              <span>{{ c.author }}</span>
              <span>{{ c.stats }}</span>
            </div>
          </div>
        </article>
      </section>
    </main>

    <nav class="dock" aria-label="底部导航">
      <button
        v-for="t in tabs"
        :key="t.id"
        class="tab"
        :class="{ 'is-selected': t.selected }"
        :aria-label="t.label"
        @click="onTab(t)"
      >
        <svg
          class="glyph"
          :class="t.selected ? 'glyph-fill' : 'glyph-muted'"
          viewBox="0 0 24 24"
          aria-hidden="true"
          v-html="t.icon"
        />
        <span class="dock-label" :class="{ 'is-selected': t.selected }">{{ t.label }}</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";

const ICONS = {
  feed: '<line x1="4" y1="6" x2="20" y2="6"></line><line x1="4" y1="12" x2="16" y2="12"></line><line x1="4" y1="18" x2="20" y2="18"></line>',
  rank: '<rect x="5" y="12" width="4" height="8" rx="1"></rect><rect x="10" y="7" width="4" height="13" rx="1"></rect><rect x="15" y="10" width="4" height="10" rx="1"></rect>',
  category: '<rect x="4" y="4" width="7" height="7" rx="1"></rect><rect x="13" y="4" width="7" height="7" rx="1"></rect><rect x="4" y="13" width="7" height="7" rx="1"></rect><rect x="13" y="13" width="7" height="7" rx="1"></rect>',
  activity: '<circle cx="12" cy="12" r="8"></circle><path d="M12 8v4l3 2"></path>',
  wallet: '<rect x="3" y="6" width="18" height="13" rx="2"></rect><path d="M3 10h18"></path><circle cx="17" cy="14.5" r="1"></circle>',
  service: '<path d="M4 13a8 8 0 0 1 16 0"></path><rect x="3" y="13" width="4" height="6" rx="2"></rect><rect x="17" y="13" width="4" height="6" rx="2"></rect>',
  home: '<path d="M3 11l9-8 9 8v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"></path>',
  discover: '<circle cx="12" cy="12" r="9"></circle><path d="M15.5 8.5l-2 5-5 2 2-5z"></path>',
  messages: '<path d="M4 7a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H10l-4 4v-4H7a3 3 0 0 1-3-3z"></path>',
  mine: '<circle cx="12" cy="8" r="4"></circle><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"></path>'
};

const keyword = ref("");
const entries = [
  { id: "feed", label: "信息流", target: "ui/feed.md", icon: ICONS.feed },
  { id: "rank", label: "排行榜", target: "ui/rank.md", icon: ICONS.rank },
  { id: "category", label: "分类", target: "ui/category.md", icon: ICONS.category },
  { id: "activity", label: "活动", target: "ui/activity.md", icon: ICONS.activity },
  { id: "wallet", label: "钱包", target: "ui/wallet.md", icon: ICONS.wallet },
  { id: "service", label: "客服", target: "ui/service.md", icon: ICONS.service }
];
const feed = [
  { id: "a1", tone: "tone-a", title: "城市漫步手账:用光影记录一条老街的下午", author: "林间摄影", stats: "2,847 赞" },
  { id: "b2", tone: "tone-b", title: "把通勤变成阅读时间的 5 个小方法", author: "深夜书房", stats: "1,273 赞" },
  { id: "c3", tone: "tone-c", title: "自烘焙入门:第一只可颂的成败实录", author: "黄油笔记", stats: "876 赞" },
  { id: "d4", tone: "tone-d", title: "周末市集寻宝:旧物改造出一张工作台", author: "木作日常", stats: "3,204 赞" }
];
const tabs = ref([
  { id: "home", label: "首页", selected: true, icon: ICONS.home },
  { id: "discover", label: "发现", selected: false, icon: ICONS.discover },
  { id: "messages", label: "消息", selected: false, icon: ICONS.messages },
  { id: "mine", label: "我的", selected: false, icon: ICONS.mine }
]);

function onSearch() {
  if (!keyword.value) {
    ElMessage.warning("请输入关键词后再搜索");
    return;
  }
  ElMessage.success("搜索: " + keyword.value);
}
function onEntry(e) {
  ElMessage("金刚区跳转目标: " + e.target + "(见 home.md §3.2)");
}
function onCard(c) {
  ElMessage("打开卡片: " + c.title);
}
function onTab(t) {
  tabs.value.forEach(x => { x.selected = (x.id === t.id); });
  ElMessage("切换到「" + t.label + "」");
}
function onMenu() {
  ElMessage("打开抽屉菜单");
}
</script>

<style>
/* token.md 硬值(亮色)注入 :root;暗色覆盖见下方 media 查询 */
:root {
  --color-brand-primary: #5B7CFA;
  --color-surface-base: #F7F8FA;
  --color-surface-card: #FFFFFF;
  --color-text-primary: #1A1D21;
  --color-text-secondary: #6B7280;
  --color-danger: #EF4444;
  --color-divider: #F0F1F3;
  --color-border-base: #E5E7EB;
  --font-size-h3: 16px;
  --font-size-body: 14px;
  --font-size-caption: 12px;
  --font-size-mini: 10px;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --line-height-base: 1.5;
  --icon-size-lg: 24px;
  --icon-size-xl: 32px;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --radius-subtle: 4px;
  --radius-rounded: 8px;
  --radius-full: 9999px;
  --border-thin: 1px;
  --motion-duration-instant: 100ms;
  --motion-duration-fast: 200ms;
  --motion-ease-default: cubic-bezier(0.25, 0.1, 0.25, 1);
  --state-hover: rgba(26, 29, 33, 0.05);
  --cover-a1: #5B7CFA;
  --cover-a2: #8AA2FC;
  --cover-b1: #3D5EDB;
  --cover-b2: #6F8CF8;
  --cover-c1: #7C93FA;
  --cover-c2: #A9BAFD;
  --cover-d1: #4C6BE8;
  --cover-d2: #93A9FA;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface-base: #141413;
    --color-surface-card: #1F1F1E;
    --color-text-primary: #F5F4ED;
    --color-text-secondary: #A8A29E;
    --color-divider: rgba(255, 255, 255, 0.06);
    --color-border-base: rgba(255, 255, 255, 0.08);
  }
}
</style>

<style scoped>
.home-page {
  max-width: 480px;
  margin: 0 auto;
  min-height: 100vh;
  background: var(--color-surface-base);
  color: var(--color-text-primary);
  font-family: "PingFang SC", "SF Pro Text", -apple-system, BlinkMacSystemFont, sans-serif;
  position: relative;
}

.glyph {
  fill: none;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.glyph-brand { stroke: var(--color-brand-primary); }
.glyph-muted { stroke: var(--color-text-secondary); }
.glyph-ink { stroke: var(--color-text-primary); }
.glyph-fill { fill: var(--color-brand-primary); stroke: none; }

.nav-bar {
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-md);
}

.nav-title {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-semibold);
}

.icon-btn {
  width: var(--icon-size-lg);
  height: var(--icon-size-lg);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  padding: 0;
}

.icon-btn .glyph { width: var(--icon-size-lg); height: var(--icon-size-lg); }

.dot {
  position: absolute;
  top: 2px;
  right: -3px;
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
  background: var(--color-danger);
}

.page-body {
  padding: var(--spacing-md) var(--spacing-lg) 96px;
}

.search-pill {
  height: 44px;
  display: flex;
  align-items: center;
  border-radius: var(--radius-full);
  background: var(--color-surface-base);
  border: var(--border-thin) solid var(--color-border-base);
  padding: 0 var(--spacing-md);
  transition: background var(--motion-duration-fast) var(--motion-ease-default);
}

.search-pill:focus-within {
  background: var(--color-surface-card);
  border-color: var(--color-brand-primary);
}

.search-pill .el-input__wrapper {
  background: transparent;
  box-shadow: none;
  padding: 0;
}

input::placeholder {
  /* placeholder token(#9CA3AF)对比度不达 4.5:1,改用 text-secondary */
  color: var(--color-text-secondary);
}

.entries {
  margin: var(--spacing-lg) 0;
}

.entry {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) 0;
  background: none;
  border: none;
  border-radius: var(--radius-subtle);
}

.entry .glyph { width: var(--icon-size-xl); height: var(--icon-size-xl); }

.entry-label {
  font-size: var(--font-size-caption);
  color: var(--color-text-secondary);
}

.feed {
  column-count: 2;
  column-gap: var(--spacing-md);
}

.card {
  break-inside: avoid;
  margin: 0 0 var(--spacing-md);
  background: var(--color-surface-card);
  border-radius: var(--radius-rounded);
  overflow: hidden;
  border: none;
  text-align: left;
  padding: 0;
  font: inherit;
  cursor: pointer;
  transition: transform var(--motion-duration-instant) var(--motion-ease-default);
}

.cover { width: 100%; aspect-ratio: 4 / 3; }

.tone-a { background: linear-gradient(160deg, var(--cover-a1), var(--cover-a2)); }
.tone-b { background: linear-gradient(160deg, var(--cover-b1), var(--cover-b2)); }
.tone-c { background: linear-gradient(160deg, var(--cover-c1), var(--cover-c2)); }
.tone-d { background: linear-gradient(160deg, var(--cover-d1), var(--cover-d2)); }

.card-body { padding: var(--spacing-sm); }

.card-title {
  margin: 0 0 var(--spacing-xs);
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-base);
  color: var(--color-text-primary);
}

.card-meta {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-caption);
  color: var(--color-text-secondary);
}

.dock {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  padding-bottom: 12px;
  background: var(--color-surface-card);
  border-top: 0.5px solid var(--color-divider);
}

.tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding-top: 8px;
  background: none;
  border: none;
}

.tab .glyph { width: var(--icon-size-lg); height: var(--icon-size-lg); }

.dock-label {
  font-size: var(--font-size-mini);
  color: var(--color-text-secondary);
}

.dock-label.is-selected {
  color: var(--color-text-primary);
  font-weight: var(--font-weight-medium);
}

.entry:hover, .icon-btn:hover { background: var(--state-hover); }
.entry:active, .tab:active, .icon-btn:active { transform: scale(0.97); }
.card:active { transform: scale(0.98); }

.icon-btn:focus-visible,
.entry:focus-visible,
.tab:focus-visible,
.card:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-brand-primary);
}

@media (prefers-reduced-motion: reduce) {
  .card, .entry, .tab, .icon-btn, .search-pill { transition: none; }
}
</style>
