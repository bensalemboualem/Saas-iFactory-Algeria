#!/usr/bin/env node
/**
 * ===================================================================
 * IAFactory CLI - Pipeline Creator
 * Command-line tool for developers
 * ===================================================================
 */

const { program } = require('commander');
const inquirer = require('inquirer');
const chalk = require('chalk');
const ora = require('ora');
const axios = require('axios');
const fs = require('fs-extra');
const path = require('path');

// Configuration
const API_BASE_URL = process.env.IAFACTORY_API || 'http://localhost:8000';
const PROJECTS_DIR = process.env.IAFACTORY_PROJECTS || path.join(process.cwd(), 'projects');

// Version
const pkg = require('./package.json');

program
  .name('iafactory')
  .description('IAFactory Algeria - Pipeline Creator CLI')
  .version(pkg.version);

/**
 * CREATE command - Create a new project
 */
program
  .command('create [name]')
  .description('Create a new project using BMAD → ARCHON → BOLT pipeline')
  .option('-d, --description <desc>', 'Project description')
  .option('-t, --type <type>', 'Project type (ecommerce, saas, blog, etc.)', 'custom')
  .option('-e, --email <email>', 'Email to receive the code')
  .action(async (name, options) => {
    console.log(chalk.green.bold('\n🚀 IAFactory Pipeline Creator\n'));

    // Prompt for missing info
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'name',
        message: 'Project name:',
        when: !name,
        validate: input => input.length > 0 || 'Project name is required'
      },
      {
        type: 'input',
        name: 'description',
        message: 'Project description:',
        when: !options.description,
        validate: input => input.length > 0 || 'Description is required'
      },
      {
        type: 'list',
        name: 'type',
        message: 'Project type:',
        when: !options.type || options.type === 'custom',
        choices: [
          { name: '🛒 E-commerce', value: 'ecommerce' },
          { name: '💼 SaaS / Dashboard', value: 'saas' },
          { name: '📝 Blog / CMS', value: 'blog' },
          { name: '📄 Landing Page', value: 'landing' },
          { name: '📱 Mobile App', value: 'mobile' },
          { name: '🎮 Game', value: 'game' },
          { name: '🔧 Custom', value: 'custom' }
        ]
      },
      {
        type: 'input',
        name: 'email',
        message: 'Your email (optional):',
        when: !options.email
      }
    ]);

    const projectData = {
      name: name || answers.name,
      description: options.description || answers.description,
      type: options.type !== 'custom' ? options.type : answers.type || 'custom',
      email: options.email || answers.email
    };

    console.log('\n' + chalk.cyan('Project Configuration:'));
    console.log(chalk.gray('  Name:'), projectData.name);
    console.log(chalk.gray('  Description:'), projectData.description);
    console.log(chalk.gray('  Type:'), projectData.type);
    if (projectData.email) {
      console.log(chalk.gray('  Email:'), projectData.email);
    }
    console.log('');

    const { confirm } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'confirm',
        message: 'Start pipeline?',
        default: true
      }
    ]);

    if (!confirm) {
      console.log(chalk.yellow('Cancelled.'));
      process.exit(0);
    }

    // Start pipeline
    const spinner = ora('Creating pipeline...').start();

    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/pipeline/create`, projectData);
      const { pipeline_id, project_dir } = response.data;

      spinner.succeed('Pipeline created!');

      console.log(chalk.green('\n✅ Pipeline started successfully!'));
      console.log(chalk.gray('  Pipeline ID:'), pipeline_id);
      console.log(chalk.gray('  Project Directory:'), project_dir);
      console.log('');

      // Poll for status
      await pollPipelineStatus(pipeline_id);

    } catch (error) {
      spinner.fail('Failed to create pipeline');
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    }
  });

/**
 * STATUS command - Check pipeline status
 */
program
  .command('status <pipeline_id>')
  .description('Check status of a running pipeline')
  .action(async (pipelineId) => {
    const spinner = ora('Fetching status...').start();

    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/pipeline/status/${pipelineId}`);
      const status = response.data;

      spinner.stop();

      console.log('\n' + chalk.cyan.bold('Pipeline Status\n'));
      console.log(chalk.gray('  Pipeline ID:'), pipelineId);
      console.log(chalk.gray('  Status:'), getStatusColor(status.status));
      console.log('');

      // BMAD
      console.log(chalk.yellow('  📋 BMAD:'), status.bmad_completed ? chalk.green('✅ Completed') : chalk.gray('⏳ Pending'));

      // ARCHON
      const archonStatus = status.archon_completed ? chalk.green('✅ Completed') :
                           status.archon_in_progress ? chalk.yellow('⏳ In Progress') :
                           chalk.gray('⏳ Pending');
      console.log(chalk.yellow('  🧠 ARCHON:'), archonStatus);

      // BOLT
      const boltStatus = status.bolt_completed ? chalk.green('✅ Completed') :
                         status.bolt_in_progress ? chalk.yellow('⏳ In Progress') :
                         chalk.gray('⏳ Pending');
      console.log(chalk.yellow('  ⚡ BOLT:'), boltStatus);

      if (status.error) {
        console.log('\n' + chalk.red('  ❌ Error:'), status.error);
      }

      if (status.completed) {
        console.log('\n' + chalk.green.bold('  ✅ Pipeline completed successfully!'));

        if (status.result) {
          console.log('\n' + chalk.cyan('  Results:'));
          if (status.result.bolt) {
            console.log(chalk.gray('    Project ID:'), status.result.bolt.project_id);
            console.log(chalk.gray('    Files:'), status.result.bolt.files_count);
          }
        }
      }

      console.log('');

    } catch (error) {
      spinner.fail('Failed to fetch status');
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    }
  });

/**
 * LIST command - List all pipelines
 */
program
  .command('list')
  .description('List all pipelines')
  .action(async () => {
    const spinner = ora('Fetching pipelines...').start();

    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/pipeline/list`);
      const { pipelines } = response.data;

      spinner.stop();

      if (pipelines.length === 0) {
        console.log(chalk.yellow('\nNo pipelines found.'));
        return;
      }

      console.log('\n' + chalk.cyan.bold(`Found ${pipelines.length} pipeline(s):\n`));

      pipelines.forEach((p, i) => {
        console.log(`${i + 1}. ${chalk.yellow(p.pipeline_id)}`);
        console.log(`   Status: ${getStatusColor(p.status)}`);
        console.log(`   Created: ${chalk.gray(new Date(p.created_at).toLocaleString())}`);
        console.log('');
      });

    } catch (error) {
      spinner.fail('Failed to fetch pipelines');
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    }
  });

/**
 * DOWNLOAD command - Download generated code
 */
program
  .command('download <project_id>')
  .description('Download generated code as ZIP')
  .option('-o, --output <path>', 'Output directory', process.cwd())
  .action(async (projectId, options) => {
    const spinner = ora('Downloading code...').start();

    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/pipeline/download/${projectId}`,
        { responseType: 'stream' }
      );

      const outputPath = path.join(options.output, `${projectId}.zip`);
      const writer = fs.createWriteStream(outputPath);

      response.data.pipe(writer);

      await new Promise((resolve, reject) => {
        writer.on('finish', resolve);
        writer.on('error', reject);
      });

      spinner.succeed('Code downloaded!');
      console.log(chalk.green('\n✅ Downloaded to:'), outputPath);

    } catch (error) {
      spinner.fail('Failed to download code');
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    }
  });

/**
 * LOGIN command - Authenticate with IAFactory API
 */
program
  .command('login')
  .description('Login to IAFactory API')
  .action(async () => {
    console.log(chalk.green.bold('\n🔐 IAFactory Login\n'));

    const { apiKey } = await inquirer.prompt([
      {
        type: 'password',
        name: 'apiKey',
        message: 'Enter your API key:',
        validate: input => input.length > 0 || 'API key is required'
      }
    ]);

    // Save API key to config file
    const configPath = path.join(process.env.HOME || process.env.USERPROFILE, '.iafactory');
    fs.ensureDirSync(configPath);

    const configFile = path.join(configPath, 'config.json');
    fs.writeJsonSync(configFile, { apiKey }, { spaces: 2 });

    console.log(chalk.green('\n✅ Logged in successfully!'));
  });

/**
 * CONFIG command - View/edit configuration
 */
program
  .command('config')
  .description('View or edit configuration')
  .option('-s, --set <key=value>', 'Set a configuration value')
  .action(async (options) => {
    const configPath = path.join(process.env.HOME || process.env.USERPROFILE, '.iafactory');
    const configFile = path.join(configPath, 'config.json');

    if (options.set) {
      const [key, value] = options.set.split('=');
      const config = fs.existsSync(configFile) ? fs.readJsonSync(configFile) : {};
      config[key] = value;
      fs.ensureDirSync(configPath);
      fs.writeJsonSync(configFile, config, { spaces: 2 });
      console.log(chalk.green(`\n✅ Set ${key} = ${value}`));
    } else {
      if (!fs.existsSync(configFile)) {
        console.log(chalk.yellow('\nNo configuration found.'));
        return;
      }

      const config = fs.readJsonSync(configFile);
      console.log('\n' + chalk.cyan.bold('Configuration:\n'));
      Object.entries(config).forEach(([key, value]) => {
        console.log(chalk.gray(`  ${key}:`), value);
      });
      console.log('');
    }
  });

/**
 * Helper: Poll pipeline status
 */
async function pollPipelineStatus(pipelineId) {
  const spinner = ora('Waiting for pipeline to complete...').start();

  let completed = false;
  let error = null;

  while (!completed && !error) {
    await new Promise(resolve => setTimeout(resolve, 5000)); // Poll every 5 seconds

    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/pipeline/status/${pipelineId}`);
      const status = response.data;

      // Update spinner text
      if (status.bmad_completed && !status.archon_completed) {
        spinner.text = 'BMAD ✅ | ARCHON ⏳ | BOLT ⏳';
      } else if (status.archon_completed && !status.bolt_completed) {
        spinner.text = 'BMAD ✅ | ARCHON ✅ | BOLT ⏳';
      } else if (status.bolt_completed) {
        spinner.text = 'BMAD ✅ | ARCHON ✅ | BOLT ✅';
      }

      completed = status.completed;
      error = status.error;

    } catch (err) {
      error = err.message;
    }
  }

  if (error) {
    spinner.fail('Pipeline failed');
    console.error(chalk.red('\nError:'), error);
    process.exit(1);
  }

  spinner.succeed('Pipeline completed!');

  console.log(chalk.green('\n✅ Your project is ready!'));
  console.log(chalk.gray('\nNext steps:'));
  console.log(chalk.gray('  1. Check status:'), `iafactory status ${pipelineId}`);
  console.log(chalk.gray('  2. Download code:'), `iafactory download ${pipelineId}`);
  console.log('');
}

/**
 * Helper: Get colored status text
 */
function getStatusColor(status) {
  switch (status) {
    case 'completed':
      return chalk.green('✅ Completed');
    case 'error':
      return chalk.red('❌ Error');
    case 'bmad_running':
    case 'archon_running':
    case 'bolt_running':
      return chalk.yellow('⏳ Running');
    default:
      return chalk.gray(status);
  }
}

// Parse arguments
program.parse(process.argv);

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
