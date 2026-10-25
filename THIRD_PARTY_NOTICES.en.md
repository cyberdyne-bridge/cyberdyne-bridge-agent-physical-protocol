# Third-Party Notices

Cyberdyne Bridge's original Kernel, protocol, drivers, and tests are **MIT**-licensed (see [`LICENSE`](LICENSE)). The third-party components, patches, runtime dependencies, and names below are not covered by that MIT grant and are used under their own terms.

**This is not legal advice.** If you distribute a combined product, have counsel review it.

---

## 1. Code and patches

| Component | Upstream | License | Location | Notes |
|---|---|---|---|---|
| Mindcraft headless patch | [mindcraft-bots/mindcraft](https://github.com/mindcraft-bots/mindcraft) | MIT | `agents/mindcraft/adapter/patches/mindcraft-headless.patch` | Lazy-load patch only; Mindcraft remains an external planner |
| Voyager state / spike patches | [MineDojo/Voyager](https://github.com/MineDojo/Voyager) | MIT | `agents/voyager/adapter/patches/*.patch` | Mineflayer bridge only; not Voyager's autonomous Python agent |
| mineflayer-mcp place patch | [swaynos/mineflayer-mcp](https://github.com/swaynos/mineflayer-mcp) | **GPL-3.0** | `agents/mcp-mineflayer/driver/patches/mineflayer-mcp-place.patch` | **Not MIT**; distributed only as a patch for an independent GPL external component |

### GPL-3.0 boundary

`mineflayer-mcp-place.patch` is a patch against GPL-3.0 upstream source. CBAP's MCP driver calls that server through a **separate stdio JSON-RPC process** and does not import GPL code into the Kernel. The patch itself is distributed under GPL-3.0; see:

```text
agents/mcp-mineflayer/driver/patches/LICENSE
third_party/licenses/mineflayer-mcp-GPL-3.0.txt
```

Do not apply the patch to a closed-source fork and then claim the whole product is MIT.

---

## 2. Runtime dependencies (not vendored)

These packages are installed through npm/pip; their source is not copied into this repository. Preserve their licenses when distributing a binary. Versions are governed by `package.json`, lockfiles, and the actual installation.

| Package | License | Purpose |
|---|---|---|
| [mineflayer](https://github.com/PrismarineJS/mineflayer) | MIT | Headless Minecraft client |
| [mineflayer-pathfinder](https://github.com/PrismarineJS/mineflayer-pathfinder) | MIT | Optional pathfinding |
| [mineflayer-collectblock](https://github.com/PrismarineJS/mineflayer-collectblock) | MIT | Block collection |
| [prismarine-physics](https://github.com/PrismarineJS/prismarine-physics) | MIT | Physics data/rules |
| Minecraft data / prismarine-* transitive dependencies | Their own MIT and other licenses | mineflayer dependency tree |
| Python standard library | PSF-2.0 | Kernel and tools |
| MCP SDK (if installed) | Upstream terms | External MCP ecosystem |

License texts are in:

```text
third_party/licenses/
```

---

## 3. External processes and services

| Name | License / terms | Relationship |
|---|---|---|
| [mineflayer-mcp](https://github.com/swaynos/mineflayer-mcp) | GPL-3.0 | Independent stdio process; not MIT code in this repo |
| [Mindcraft](https://github.com/mindcraft-bots/mindcraft) | MIT | External agent; this repo contains only an adapter/patch |
| [Voyager](https://github.com/MineDojo/Voyager) | MIT | External agent bridge; planner not wired |
| Minecraft Java / Mojang / Microsoft | Proprietary | Game/server not distributed; interoperability only |
| DeepSeek / Qwen models | Their model terms | Model weights not distributed; names/compatibility only |
| xdg-desktop-portal / Wayland / X11 | Their open-source licenses | Local input/screenshot backends; not code from this repo |

### Media and screenshots

```text
assets/DeepSeek-skin.png
site/assets/deepseek-skin.png
```

This is a community-style Minecraft skin asset, not official Mojang material. Verify its source and permission before redistributing it.

CBAP architecture diagrams, CBAP OS screenshots, and terminal captures were produced by this project. Minecraft imagery and names in screenshots are used only to explain interoperability and do not sublicense game assets.

---

## 4. Names and trademarks

See [`TRADEMARKS.en.md`](TRADEMARKS.en.md).

```text
Minecraft is a trademark of Mojang Studios / Microsoft.
This project is not an official Mojang, Microsoft, NetEase, DeepSeek, Qwen,
Mindcraft, Voyager, or mineflayer-mcp project and is not endorsed by them.
```

---

## 5. Original-code license

The MIT text in the root `LICENSE` applies to original CBAP code. Third-party patches, dependencies, and names do not change license because they are referenced here.

If you distribute a modified version of this repository:

```text
keep the root LICENSE
keep THIRD_PARTY_NOTICES.md
keep third_party/licenses/
keep the license next to each patch where applicable
do not remove upstream copyright headers
```

---

## 6. Disclaimer

See [`DISCLAIMER.en.md`](DISCLAIMER.en.md) and [`SECURITY.en.md`](SECURITY.en.md).
