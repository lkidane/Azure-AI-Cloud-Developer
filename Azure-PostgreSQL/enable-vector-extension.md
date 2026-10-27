## Enable Vector Extension and Setup RAG Parent Table


### Enabling PG Vector Extension

1) Go to `Server Parameters` in Azure portal and enable `vector` in `azure.extensions`

2) Enable vector extension: `CREATE EXTENSION IF NOT EXISTS vector;`

3) Check installation: `SELECT * FROM pg_extension WHERE extname = 'vector';`

### Creating the RAG Parent Table

Create Schema:
```sql
CREATE SCHEMA RAG;
```

Create the Parent Table:
```
CREATE TABLE RAG.ESG_TextData (
    RecordID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    CompanyID INT,
    CompanyName VARCHAR(100),

    ReviewText TEXT,
    SustainabilityReport TEXT,

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Add Data:
```sql
INSERT INTO RAG.ESG_TextData
(
    CompanyID,
    CompanyName,
    ReviewText,
    SustainabilityReport
)
VALUES

(
    1,
    'GreenSteel Ltd',
    'The company has improved its emissions significantly but still lacks transparency.',
    'GreenSteel Ltd has undertaken a comprehensive transformation program aimed at reducing its environmental footprint across all major operations. Over the past financial year, the company achieved a 22% reduction in Scope 1 emissions through process optimization and fuel switching initiatives. A significant portion of this reduction was driven by the gradual replacement of coal-based furnaces with electric arc furnaces powered by renewable energy sources. Additionally, GreenSteel has expanded its solar energy capacity at manufacturing sites, contributing to a 15% reduction in overall grid dependency.

The company has also invested in advanced monitoring systems to track emissions in real time, enabling better compliance with environmental regulations and internal sustainability targets. On the social front, GreenSteel has improved worker safety standards and launched community engagement programs focused on environmental awareness. However, challenges remain in addressing Scope 3 emissions, particularly those arising from raw material sourcing and logistics. The company has initiated supplier engagement programs and aims to achieve carbon neutrality by 2035.'
),

(
    2,
    'EcoLogistics',
    'Excellent sustainability practices and strong ESG governance.',
    'EcoLogistics has positioned itself as a leader in sustainable transportation and supply chain optimization. Over the past year, the company has made significant progress by transitioning a large portion of its fleet to electric and hybrid vehicles. Approximately 40% of its last-mile delivery operations are now electrified, resulting in a measurable decrease in fuel consumption and greenhouse gas emissions.

The company has also implemented AI-driven route optimization systems that minimize travel distance and idle time, further contributing to emission reductions. Additionally, EcoLogistics has partnered with renewable energy providers to power its charging infrastructure. These initiatives have collectively resulted in a 30% reduction in Scope 1 and Scope 2 emissions. While scaling sustainability practices across international markets remains a challenge, the company is committed to achieving net-zero emissions by 2040 through innovation and strategic partnerships.'
),

(
    3,
    'UrbanRetail',
    'Poor waste management practices and inconsistent ESG reporting.',
    'UrbanRetail has taken initial steps toward integrating sustainability into its operations, though progress remains uneven. During the reporting period, the company introduced recycling initiatives aimed at reducing packaging waste and promoting circular economy practices. These efforts have resulted in modest improvements, particularly in high-traffic urban stores.

The company has also begun transitioning to energy-efficient lighting and HVAC systems, contributing to incremental reductions in energy consumption. However, UrbanRetail continues to face challenges in supply chain transparency, with limited oversight into vendor sustainability practices. Scope 3 emissions remain largely unaddressed, representing a critical gap in its ESG strategy. Governance improvements include the release of its first sustainability report, though data quality and consistency require further refinement. The company plans to invest in digital tracking systems and define clearer ESG targets in the coming years.'
),

(
    4,
    'FutureEnergy Corp',
    'Strong renewable focus but execution delays are concerning.',
    'FutureEnergy Corp has focused heavily on expanding its renewable energy portfolio, particularly in solar and wind energy projects. Over the past year, the company increased its renewable generation capacity by over 35%, significantly reducing its dependence on fossil fuels. Investments in grid modernization and battery storage systems have improved energy reliability and efficiency.

The company has also introduced advanced analytics platforms to monitor energy production and environmental impact in real time. However, several large-scale projects have experienced delays due to regulatory approvals and supply chain disruptions. While the long-term vision remains strong, execution challenges have impacted short-term progress. FutureEnergy continues to enhance its ESG disclosures and stakeholder engagement efforts, with a target of achieving full renewable energy transition by 2030.'
),

(
    5,
    'PetroTrans Ltd',
    'Sustainability commitments exist but actual impact seems limited.',
    'PetroTrans Ltd has introduced sustainability initiatives aimed at reducing the environmental impact of its operations, particularly within refining and transportation segments. The company has invested in carbon capture and storage technologies and implemented efficiency improvements across its facilities. These efforts have contributed to a reduction in emissions intensity, though absolute emissions remain high.

PetroTrans has also initiated pilot projects exploring alternative fuels and renewable energy integration. Despite these efforts, the company continues to face criticism for slow progress and reliance on traditional fossil fuel operations. Governance practices have improved, with enhanced ESG reporting and stakeholder communication. However, investors and regulators are increasingly demanding more aggressive action. PetroTrans aims to transition toward a more diversified energy portfolio over the next decade while balancing economic and environmental priorities.'
);
```
CREATE EXTENSION IF NOT EXIST vector;

Create the Vector Table:
```sql
CREATE TABLE RAG.ESG_Chunks (

    ChunkID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    RecordID INT NOT NULL,

    CompanyName VARCHAR(100),

    ChunkText TEXT,

    ChunkEmbedding VECTOR(1536),

    CONSTRAINT FK_ESG_Chunks_Record
        FOREIGN KEY (RecordID)
        REFERENCES RAG.ESG_TextData(RecordID)
        ON DELETE CASCADE
);
```