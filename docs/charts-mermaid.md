### Charts

These are the mermaid charts in the design doc. I used the [mermaid live editor](https://mermaidjs.github.io/mermaid-live-editor) and screenshots.

---
Stages:

```
graph LR
A>Site Mapping]
B>Ad Listings]
C>Ads]
D>Processing]
A---B
B---C
C---D
style A fill:#ded,stroke:#333
style B fill:#ded,stroke:#333
style C fill:#ded,stroke:#333
style D fill:#ded,stroke:#333
```

---

Site Mapping:

```
graph TD
A(Site Map Loader)--> B[\Site Map Crawl Queue/]
B-->C(Site Map Crawler)
C-->D[\Site Map Parser Queue/]
D-->E(Site Map Parse)
E-->F{{Ad Listing Azure Table}}

style A fill:#def,stroke:#333
style C fill:#def,stroke:#333
style E fill:#def,stroke:#333

style B fill:#fef,stroke:#333
style D fill:#fef,stroke:#333

style F fill:#ffa,stroke:#333
```

---
Ad Listings:

```
graph TD
A("Ad Listing Loader")
A--> B[\Ad Listing Crawl Queue/]
B-->C(Ad Listing Crawler)
C-->D[\Ad Listing Parser Queue/]
D-->E(Ad Listing Parser)
E-.check if ad url  is already crawled -.-F{{Ad Listing Azure Table}}
E-- new ad url -->G[\Ad Crawl Queue/]
style A fill:#def,stroke:#333
style C fill:#def,stroke:#333
style E fill:#def,stroke:#333

style B fill:#fef,stroke:#333
style D fill:#fef,stroke:#333
style G fill:#fef,stroke:#333

style F fill:#ffa,stroke:#333
```

---
Ads:

```
graph TD
A[\Ad Crawl Queue/]
A -->B(Ad Crawler)
B-->C[\Ad Parser Queue/]
B-->H[/Ad HTML Blob Store\]
C-->D(Ad Listing Parser)
D-->G[\Processing Queue/]
D-->E[\Image Crawl Queue/]
E-->F(Image Crawler)
F-->I[/Image Blob Store\]
J{{Ads Azure Table}}
K{{Images Azure Table}}
B-. mark ad crawled -.-J
D-. check image crawled -.-K
D-. mark ad parsed -.-J
F-. mark image crawled -.-K


style A fill:#fef,stroke:#333
style C fill:#fef,stroke:#333
style G fill:#fef,stroke:#333
style E fill:#fef,stroke:#333

style B fill:#def,stroke:#333
style D fill:#def,stroke:#333
style F fill:#def,stroke:#333

style J fill:#ffa,stroke:#333
style K fill:#ffa,stroke:#333

style H fill:#fda,stroke:#333
style I fill:#fda,stroke:#333
```

---
Processing:

```
graph TD
A[\Processing Queue/]
A -->B(Processor)
B-->C((CosmosDB))
style A fill:#fef,stroke:#333
style B fill:#def,stroke:#333
style C fill:#ded,stroke:#333
```
