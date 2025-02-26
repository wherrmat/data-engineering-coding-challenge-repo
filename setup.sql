SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[hired_employees](
	[id] [int] NOT NULL,
	[name] [nvarchar](200) NULL,
	[datetime] [nvarchar](200) NULL,
	[department_id] [int] NULL,
	[job_id] [int] NULL
)

GO
CREATE TABLE [dbo].[departments](
	[id] [int] NOT NULL,
	[department] [nvarchar](200) NULL,
)

GO
CREATE TABLE [dbo].[jobs](
	[id] [int] NOT NULL,
	[job] [nvarchar](200) NULL,
)