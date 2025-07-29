# import pandas as pd

# # Load Excel files
# df1 = pd.read_excel("karnataka_tomato_2015_2020.xlsx")
# df2 = pd.read_excel("karnataka_tomato_2021_2025.xlsx")

# # Combine them
# combined_df = pd.concat([df1, df2], ignore_index=True)

# # Sort by date if applicable
# if "Arrival_Date" in combined_df.columns:
#     combined_df["Arrival_Date"] = pd.to_datetime(combined_df["Arrival_Date"], errors='coerce')
#     combined_df = combined_df.sort_values(by="Arrival_Date")

# # Save final file
# combined_df.to_excel("karnataka_tomato_2015_2025_combined.xlsx", index=False)


import pandas as pd
import glob

# # Path to your downloaded files folder (adjust this)
# folder_path = "E:/commodity market data/New folder/Mondi Historical Price Data/*.xlsx"  

# all_files = glob.glob(folder_path)

# combined_df = pd.DataFrame()

# for file in all_files:
#     print(f"✅ Processing: {file}")
#     df = pd.read_excel(file)
#     combined_df = pd.concat([combined_df, df], ignore_index=True)

# # Sort by Arrival_Date if present
# if "Arrival_Date" in combined_df.columns:
#     combined_df["Arrival_Date"] = pd.to_datetime(combined_df["Arrival_Date"], errors='coerce')
#     combined_df = combined_df.sort_values(by="Arrival_Date").reset_index(drop=True)

# # Save the combined file
# combined_df.to_excel("combined_mondi_data.xlsx", index=False)
# print("✅ All files combined successfully!")


folder_path = "E:/commodity market data/New folder/Mondi Historical Price Data/*.xlsx"
all_files = glob.glob(folder_path)

unique_files = set(all_files)

print(f"Total files found: {len(all_files)}")
print(f"Unique files found: {len(unique_files)}")

df = pd.read_excel("E:/commodity market data/Commodity_market_data/combined_mondi_data.xlsx")
print(f"✅ Total rows in combined Excel: {len(df)}")


folder_path = "E:/commodity market data/New folder/Mondi Historical Price Data/*.xlsx"
all_files = glob.glob(folder_path)

total_rows = 0

for file in sorted(all_files):
    df = pd.read_excel(file)
    row_count = len(df)
    print(f"{file} --> {row_count} rows")
    total_rows += row_count

print(f"\n✅ Total rows across all files: {total_rows}")


